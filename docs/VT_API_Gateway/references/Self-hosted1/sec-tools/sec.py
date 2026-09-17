#!/usr/bin/env python3
"""
sec.py — Dependency-Track / SonarQube 취약점·이슈 조회 도구

사내 빌드 서버의 DT·SonarQube 에 REST API 로 직접 붙는다. SSH 불필요.
표준 라이브러리만 쓴다(추가 설치 없음). Python 3.8+.

사용법:
    ./sec.py check                  설정·연결·권한 점검
    ./sec.py projects [검색어]      DT·SonarQube 프로젝트 검색
    ./sec.py vulns <프로젝트>       DT 취약점 상세
    ./sec.py issues <프로젝트>      SonarQube 이슈
    ./sec.py hotspots <프로젝트>    SonarQube security hotspot
    ./sec.py analyze <프로젝트>     DT 재분석 요청

    --json 을 붙이면 기계가 읽는 형식으로 출력한다(AI 도구에 넘길 때 유용).

<프로젝트> 는 이름 일부면 된다. 여러 개가 걸리면 목록을 보여 준다.
"""
import argparse, base64, json, os, sys, urllib.error, urllib.parse, urllib.request

if sys.version_info < (3, 8):
    sys.exit(f"Python 3.8 이상이 필요하다 (현재 {sys.version.split()[0]}).")

# Windows 콘솔 기본 코드페이지에서 한글이 깨지는 것을 막는다.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# realpath 를 쓴다 — ~/.local/bin/sec 같은 심링크로 불려도 .env 를 찾아야 한다.
HERE = os.path.dirname(os.path.realpath(__file__))


# ── 설정 ────────────────────────────────────────────────────────────
def load_env():
    """.env 파일과 환경변수에서 설정을 읽는다. 환경변수가 우선."""
    cfg = {}
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    for k in ("DTRACK_URL", "DTRACK_API_KEY", "SONAR_URL", "SONAR_TOKEN"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    cfg.setdefault("DTRACK_URL", "http://dtrack.ewoosoft.com:8081")
    cfg.setdefault("SONAR_URL", "http://sqube.ewoosoft.com")
    return cfg


CFG = load_env()


def die(msg, hint=None):
    print(f"오류: {msg}", file=sys.stderr)
    if hint:
        print(f"      {hint}", file=sys.stderr)
    sys.exit(1)


# ── HTTP ────────────────────────────────────────────────────────────
def request(url, headers, method="GET", timeout=30):
    req = urllib.request.Request(url, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return r.status, dict(r.headers), body
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        die(f"{url} 에 연결할 수 없다: {e}",
            "사내망에 있는지, URL 이 맞는지 확인할 것.")


def dt(path, method="GET"):
    if not CFG.get("DTRACK_API_KEY"):
        die("DTRACK_API_KEY 가 없다.", "sec-tools/.env 에 값을 넣을 것. README 1단계 참조.")
    url = CFG["DTRACK_URL"].rstrip("/") + path
    st, hd, body = request(url, {"X-Api-Key": CFG["DTRACK_API_KEY"]}, method)
    if st == 401:
        die("DT 인증 실패(401).", "DTRACK_API_KEY 를 확인할 것.")
    if st == 403:
        die("DT 권한 부족(403).", "이 API 키에 조회 권한이 없다. 관리자에게 문의할 것.")
    if st >= 400:
        die(f"DT 오류 {st}: {body[:200].decode('utf-8', 'replace')}")
    return json.loads(body) if body else None, hd


def sq(path):
    if not CFG.get("SONAR_TOKEN"):
        die("SONAR_TOKEN 이 없다.", "sec-tools/.env 에 값을 넣을 것. README 2단계 참조.")
    url = CFG["SONAR_URL"].rstrip("/") + path
    auth = base64.b64encode(f"{CFG['SONAR_TOKEN']}:".encode()).decode()
    st, hd, body = request(url, {"Authorization": f"Basic {auth}"})
    if st == 401:
        die("SonarQube 인증 실패(401).", "SONAR_TOKEN 을 확인할 것.")
    if st == 403:
        return None  # 권한 없음 — 호출부에서 처리
    if st >= 400:
        die(f"SonarQube 오류 {st}: {body[:200].decode('utf-8', 'replace')}")
    return json.loads(body) if body else None


# ── 프로젝트 해석 ───────────────────────────────────────────────────
def dt_find(term):
    """이름 일부로 DT 프로젝트를 찾는다. UUID 를 그대로 줘도 된다."""
    term = term.strip()
    if len(term) == 36 and term.count("-") == 4:
        p, _ = dt(f"/api/v1/project/{term}")
        return [p]
    data, _ = dt("/api/v1/project?pageSize=500")
    t = term.lower()
    hits = [p for p in data if t in p["name"].lower()]
    # 이름이 정확히 일치하는 것이 있으면 그것만 쓴다.
    exact = [p for p in hits if p["name"].lower() == t]
    return exact or hits


def sq_find(term):
    term = term.strip()
    data = sq("/api/components/search?qualifiers=TRK&ps=500")
    if data is None:
        return []
    t = term.lower()
    hits = [c for c in data.get("components", [])
            if t in c["key"].lower() or t in c.get("name", "").lower()]
    exact = [c for c in hits if c["key"].lower() == t or c.get("name", "").lower() == t]
    return exact or hits


def pick(matches, label, key_fn, term):
    if not matches:
        die(f"{label} 에서 '{term}' 에 해당하는 프로젝트를 못 찾았다.",
            "./sec.py projects 로 목록을 확인할 것.")
    if len(matches) > 1:
        print(f"'{term}' 에 {len(matches)}개가 걸린다. 더 좁혀서 지정할 것.\n", file=sys.stderr)
        for m in matches[:20]:
            print(f"  {key_fn(m)}", file=sys.stderr)
        sys.exit(2)
    return matches[0]


# ── 명령 ────────────────────────────────────────────────────────────
def cmd_check(args):
    ok = True
    print("설정 점검\n")

    print(f"  DTRACK_URL      {CFG['DTRACK_URL']}")
    print(f"  DTRACK_API_KEY  {'설정됨' if CFG.get('DTRACK_API_KEY') else '(비어 있음)'}")
    print(f"  SONAR_URL       {CFG['SONAR_URL']}")
    print(f"  SONAR_TOKEN     {'설정됨' if CFG.get('SONAR_TOKEN') else '(비어 있음)'}")
    print()

    st, _, body = request(CFG["DTRACK_URL"].rstrip("/") + "/api/version", {})
    if st == 200:
        v = json.loads(body).get("version")
        print(f"  [OK] Dependency-Track 연결 — v{v}")
    else:
        print(f"  [실패] Dependency-Track 연결 (http={st})"); ok = False

    if CFG.get("DTRACK_API_KEY"):
        url = CFG["DTRACK_URL"].rstrip("/") + "/api/v1/project?pageSize=1"
        st, hd, _ = request(url, {"X-Api-Key": CFG["DTRACK_API_KEY"]})
        if st == 200:
            print(f"  [OK] DT 인증 — 프로젝트 {hd.get('X-Total-Count', '?')}개 조회 가능")
        else:
            print(f"  [실패] DT 인증 (http={st})"); ok = False
    else:
        print("  [건너뜀] DT 인증 — 키 없음"); ok = False

    st, _, body = request(CFG["SONAR_URL"].rstrip("/") + "/api/system/status", {})
    if st == 200:
        print(f"  [OK] SonarQube 연결 — {json.loads(body).get('status')}")
    else:
        print(f"  [실패] SonarQube 연결 (http={st})"); ok = False

    if CFG.get("SONAR_TOKEN"):
        d = sq("/api/users/current")
        if d:
            print(f"  [OK] SonarQube 인증 — {d.get('login')}")
            probe = sq("/api/components/search?qualifiers=TRK&ps=1")
            comps = (probe or {}).get("components", [])
            if comps:
                k = urllib.parse.quote(comps[0]["key"])
                h = sq(f"/api/hotspots/search?projectKey={k}&ps=1")
                print("  [OK] hotspot 조회 권한 있음" if h is not None
                      else "  [제한] hotspot 조회 권한 없음 — issues 는 되지만 hotspots 는 안 된다")
            else:
                print("  [건너뜀] hotspot 권한 — 조회 가능한 프로젝트가 없다")
        else:
            print("  [실패] SonarQube 인증"); ok = False
    else:
        print("  [건너뜀] SonarQube 인증 — 토큰 없음"); ok = False

    print()
    print("모두 정상이다. ./sec.py projects 로 시작할 것." if ok
          else "위 [실패] 항목을 README 에 따라 해결할 것.")
    return 0 if ok else 1


def cmd_projects(args):
    term = args.term or ""
    out = {"dependency_track": [], "sonarqube": []}

    if not CFG.get("DTRACK_API_KEY") and not CFG.get("SONAR_TOKEN"):
        die("DTRACK_API_KEY 와 SONAR_TOKEN 이 모두 비어 있다.",
            f"{os.path.join(HERE, '.env')} 를 확인할 것. ./sec.py check 로 점검할 수 있다.")
    if not CFG.get("DTRACK_API_KEY"):
        print("경고: DTRACK_API_KEY 가 없어 Dependency-Track 은 건너뛴다.", file=sys.stderr)
    if not CFG.get("SONAR_TOKEN"):
        print("경고: SONAR_TOKEN 이 없어 SonarQube 는 건너뛴다.", file=sys.stderr)

    if CFG.get("DTRACK_API_KEY"):
        data, _ = dt("/api/v1/project?pageSize=500")
        for p in data:
            if term.lower() in p["name"].lower():
                m = p.get("metrics") or {}
                out["dependency_track"].append({
                    "name": p["name"], "version": p.get("version"), "uuid": p["uuid"],
                    "vulnerabilities": m.get("vulnerabilities"),
                    "last_bom_import": p.get("lastBomImport"),
                })
    if CFG.get("SONAR_TOKEN"):
        for c in sq_find(term):
            out["sonarqube"].append({"key": c["key"], "name": c.get("name")})

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 0

    dtl = [p for p in out["dependency_track"] if p["last_bom_import"]]
    print(f"Dependency-Track — {len(dtl)}개 (BOM 있는 것만)\n")
    for p in sorted(dtl, key=lambda x: -(x["vulnerabilities"] or 0)):
        print(f"  {(p['name'] + ' ' + (p['version'] or '')).strip():<44} 취약점 {p['vulnerabilities'] or 0:>4}   {p['uuid']}")
    print(f"\nSonarQube — {len(out['sonarqube'])}개\n")
    for c in sorted(out["sonarqube"], key=lambda x: x["key"]):
        print(f"  {c['key']}")
    return 0


def cmd_vulns(args):
    p = pick(dt_find(args.term), "Dependency-Track",
             lambda m: f"{m['name']} {m.get('version') or ''}".strip(), args.term)
    findings, _ = dt(f"/api/v1/finding/project/{p['uuid']}")

    rows = []
    for f in findings:
        c, v, a = f.get("component", {}), f.get("vulnerability", {}), f.get("analysis", {})
        rows.append({
            "severity": v.get("severity"),
            "vuln_id": v.get("vulnId"), "source": v.get("source"),
            "cvss": v.get("cvssV3BaseScore") or v.get("cvssV2BaseScore"),
            "component": c.get("name"), "version": c.get("version"), "purl": c.get("purl"),
            "suppressed": bool(a.get("isSuppressed")), "state": a.get("state"),
            "title": (v.get("title") or "").strip() or None,
        })
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4, "UNASSIGNED": 5}
    rows.sort(key=lambda r: (order.get(r["severity"], 9), r["component"] or ""))

    if args.json:
        print(json.dumps({"project": {"name": p["name"], "version": p.get("version"),
                                      "uuid": p["uuid"]}, "findings": rows},
                         ensure_ascii=False, indent=2)); return 0

    print(f"{p['name']} {p.get('version') or ''} — 취약점 {len(rows)}건\n")
    if not rows:
        print("  없음"); return 0
    print(f"  {'심각도':<10} {'취약점 ID':<20} {'CVSS':>5}  {'컴포넌트':<34} 출처")
    print(f"  {'-'*10} {'-'*20} {'-'*5}  {'-'*34} {'-'*8}")
    for r in rows:
        mark = " (억제됨)" if r["suppressed"] else ""
        comp = f"{r['component']}@{r['version']}"
        print(f"  {r['severity'] or '-':<10} {r['vuln_id'] or '-':<20} {str(r['cvss'] or '-'):>5}  {comp[:34]:<34} {r['source'] or '-'}{mark}")
    return 0


def cmd_issues(args):
    m = pick(sq_find(args.term), "SonarQube", lambda x: x["key"], args.term)
    key = m["key"]
    d = sq(f"/api/issues/search?componentKeys={urllib.parse.quote(key)}&ps=200&resolved=false")
    if d is None:
        die("SonarQube 이슈 조회 권한이 없다.", "개인 토큰으로 다시 시도할 것.")
    rows = [{"severity": i.get("severity"), "type": i.get("type"), "rule": i.get("rule"),
             "file": (i.get("component") or "").split(":")[-1], "line": i.get("line"),
             "message": i.get("message")} for i in d.get("issues", [])]
    order = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}
    rows.sort(key=lambda r: order.get(r["severity"], 9))

    if args.json:
        print(json.dumps({"project": key, "total": d.get("total"), "issues": rows},
                         ensure_ascii=False, indent=2)); return 0

    print(f"{key} — 미해결 이슈 {d.get('total')}건 (최대 200건 표시)\n")
    for r in rows:
        loc = f"{r['file']}:{r['line']}" if r["line"] else r["file"]
        print(f"  {r['severity'] or '-':<9} {r['type'] or '-':<12} {loc[:44]:<44} {(r['message'] or '')[:60]}")
    return 0


def cmd_hotspots(args):
    m = pick(sq_find(args.term), "SonarQube", lambda x: x["key"], args.term)
    key = m["key"]
    d = sq(f"/api/hotspots/search?projectKey={urllib.parse.quote(key)}&ps=200")
    if d is None:
        die("hotspot 조회 권한이 없다.",
            "Jenkins 자동화 토큰으로는 막힌다. 개인 계정 토큰을 쓸 것.")
    rows = [{"status": h.get("status"), "probability": h.get("vulnerabilityProbability"),
             "file": (h.get("component") or "").split(":")[-1], "line": h.get("line"),
             "message": h.get("message")} for h in d.get("hotspots", [])]
    if args.json:
        print(json.dumps({"project": key, "hotspots": rows}, ensure_ascii=False, indent=2)); return 0
    print(f"{key} — security hotspot {len(rows)}건\n")
    for r in rows:
        loc = f"{r['file']}:{r['line']}" if r["line"] else r["file"]
        print(f"  {r['probability'] or '-':<8} {r['status'] or '-':<12} {loc[:44]:<44} {(r['message'] or '')[:56]}")
    return 0


def cmd_analyze(args):
    p = pick(dt_find(args.term), "Dependency-Track",
             lambda m: f"{m['name']} {m.get('version') or ''}".strip(), args.term)
    dt(f"/api/v1/finding/project/{p['uuid']}/analyze", method="POST")
    print(f"{p['name']} {p.get('version') or ''} 재분석을 요청했다. 몇 분 뒤 ./sec.py vulns 로 확인할 것.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="DT / SonarQube 취약점·이슈 조회",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    ap.add_argument("--json", action="store_true", help="기계가 읽는 형식으로 출력")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="설정·연결·권한 점검")
    p = sub.add_parser("projects", help="프로젝트 검색"); p.add_argument("term", nargs="?")
    for name, help_ in (("vulns", "DT 취약점"), ("issues", "SQ 이슈"),
                        ("hotspots", "SQ security hotspot"), ("analyze", "DT 재분석 요청")):
        s = sub.add_parser(name, help=help_); s.add_argument("term")
    args = ap.parse_args()
    return globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    sys.exit(main())
