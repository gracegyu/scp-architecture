# Web Section View / Cloud Web Viewer v1.3.2 Section 모듈 — 주간회의 Agenda

> **용도:** Section Layout(Section 모듈) 개발·Spec·인계 진행을 주간 회의에서 공유·결정할 때 사용한다.  
> **참고 형식:** [VT API Gateway 주간회의 Agenda](../../VT_API_Gateway/08.VT_API_Gateway/주간회의-Agenda.md)  
> **정본 문서:** `Cloud Web Viewer v1.3.2/` — [개발계획](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-개발계획.md) · [OnePager Spec](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-Spec-v1.3.2-OnePager.md) · [Claude Code 작업 가이드](./Cloud%20Web%20Viewer%20v1.3.2/Claude%20Code%20작업%20가이드.md)

---

## 작성 규칙 (템플릿)

매주 **회의 직전**에 아래 블록을 **파일 맨 아래에 추가**한다. 이전 주 스냅샷은 **삭제하지 않고 보존**(GW Agenda와 동일).

### 주차 블록 구조

| 섹션 | 용도 |
|------|------|
| **이번 주 진행** | 지난 주 이후 완료·진행 중 작업 (불릿) |
| **논의 사항** | 결정·확인이 필요한 항목 — `R1`, `R2` … |
| **공유 사항** | 결정 아님 — 진행·일정·리스크 공유 — `S1`, `S2` … |
| **이월 논의 사항** | 미결 표 — `#` · 항목 · 타입 · 상태 |

### 타입 (논의·이월 표)

| 타입 | 의미 |
|------|------|
| [확정] | 기결정 공식 확정·승인 |
| [논의] | 방향·범위 결정 필요 |
| [정보] | 추가 입력·자료·담당자 확보 |
| [선결] | 구현·Spec 착수 전 반드시 필요 |

### 논의 항목 작성 패턴 (복사용)

```markdown
# Cloud Web Viewer v1.3.2 Section 모듈 — M/D 주간회의 Agenda

> 이전 주(M/D) 스냅샷은 위에 보존. 아래는 이번 주 최신 스냅샷.

- 이번 주 진행 (M/D 이후)
  - (완료·진행 항목)
  -

- 논의 사항 (신규 · 이전 주 후속)

  - **R1. (제목)** — (한 줄 요약). **결정 요청:** …
    - (결정) …
    - **성격:** [논의] / [확정] / [정보]

- 공유 사항 (결정 아님)

  - **S1. (제목)** — …

- 이월 논의 사항 (미결 — 계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 1 | … | [논의] | … |

  - **차주 이월 후보:** R1 미확정 시 다음 주 이월.
```

### 관련 링크 (회의 전 확인)

| 항목 | 위치 |
|------|------|
| MMI v0.9.1 | `Cloud Web Viewer v1.3.2/기획·요구사항/MMI/MMI.md` |
| UI 시각 정본 | `.../기획·요구사항/MMI/media/image23.png` |
| 기획 답변 | [PLAN-1287.md](./Cloud%20Web%20Viewer%20v1.3.2/기획·요구사항/PLAN-1287.md) |
| 개발실 리뷰 | [MMI_개발실리뷰.md](./Cloud%20Web%20Viewer%20v1.3.2/검토/MMI_개발실리뷰.md) |
| PoC 결과 | `PoC/Phase1/` … `Phase5/` |
| 구현 레포 | `scp-section-poc` |
| CW 참조·link | `cloudwebviewer` |
| EzCloud Test (MPR·툴바) | https://container.test.ezcloud.ezcld.net/ |

---

# Cloud Web Viewer v1.3.2 Section 모듈 — 7/16 주간회의 Agenda

> **첫 주간 스냅샷.** PoC Phase 1~5 완료 이후, Section 모듈 Spec 정제 단계 착수 시점.

- 이번 주 진행 (7/10 이후 · 회의 전까지 갱신)

  - Web Section View **PoC Phase 1~5** 기술 검증 완료 (`scp-section-poc`)
  - Section 모듈 **문서 3종** 정합 — 개발계획 v0.8 · OnePager v0.6(초안) · Claude Code 작업 가이드 v1.8
  - **개발 레포 방안 1 확정** — `scp-section-poc` 계속 + `@cloudwebviewer/core` pnpm link (소스 복사 금지)
  - **화면 3분할** 범위 정리 — (1) Toolbar link · (2) MPR/Section 데모 · (3) Section 뷰 = 인계 핵심
  - `section.code-workspace` — 문서·코드·CW·EzCloud 8레포 동시 열람
  - **다음 작업:** Claude Code로 OnePager Spec 정제 (개발계획 §3.7, 가이드 §16.0)

- 논의 사항

  - **R1. Section 모듈 Spec 리뷰 일정·참석자** — OnePager 정제 완료 후 기획(Jessi)·CW Viewer 담당자 리뷰가 필요하다. **결정 요청:** 리뷰 시점(목표 주)·필수 참석·승인 기준(OnePager만 vs MMI 매핑 표 포함).
    - **성격:** [논의]

  - **R2. B/L 자동 판정 알고리즘 기획 confirm** — PLAN-1287 Raymond 초안 반영(OnePager §4). 기획 신규 정의 목표(7/10 comment 91A) 대비 **confirm 지연 시** 구현 착수 범위 — 자동 판정 보류·L/B Switching만 먼저 할지.
    - **성격:** [논의] · 담당: 기획(Jessi)

  - **R3. Save Project Section 모듈 범위** — MMI 1.14 포함이나, Section 모듈 단독 **데이터 모델+데모** vs 접목 시 CW prj I/O 완성 중 어디까지 Spec에 명시할지. CW 팀 합의 필요.
    - **성격:** [논의] · 담당: Raymond + CW Viewer

- 공유 사항

  - **S1. 현재 단계 (개발계획 §4)** — `PoC 완료 → [지금] Spec 정제 → Spec 리뷰 → §10 환경 정렬 → 구현 → 인계 → CW 접목`
  - **S2. Claude Code 운영** — cwd = `scp-section-poc`, 문서는 `scp-architecture/.../v1.3.2/` 절대경로. 첫 프롬프트 = 가이드 §16.0.
  - **S3. 일정 스냅샷 (잠정)** — Spec 정제(7월 중) → 환경 정렬·구현 착수(정제·리뷰 후). Slice 스크롤 성능은 **구현 초기 벤치마크**(별도 PoC 아님). Raymond **VT API Gateway 병행(부분투입)** — Section 일정은 주간 갱신.

    ```mermaid
    gantt
        title Section 모듈 — 잠정 일정 (7/16 스냅샷)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:2px,stroke:#d33,opacity:0.5

        section 문서·Spec
        OnePager Spec 정제 (Claude Code)     :active, spec, 2026-07-10, 14d
        Spec 리뷰 (기획 + CW)                :specrv, after spec, 7d

        section 환경·구현 (scp-section-poc)
        cloudwebviewer 환경 정렬 + link      :env, after specrv, 7d
        Section 모듈 MMI 정합 구현           :impl, after env, 35d
        Slice 스크롤 벤치마크 (구현 초기)     :bench, after impl, 7d

        section 인계
        패키지·API·데모 인계                 :hand, after bench, 7d
        CW Viewer 접목 (CW 팀)               :integ, after hand, 14d
    ```

  - **S4. Known gaps (Spec 정제 시 명시)** — EzCloud에 MPR/Section 토글·Section 본문 미탑재(예상) · Arrow 툴 CW 미구현 · B/L confirm 대기 · Overlay Normal 허용 오차 TBD.

- 이월 논의 사항 (7/16 기준 · 미결)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 1 | B/L 자동 판정 최종 알고리즘 | [논의] | Raymond 초안 → Jessi confirm 대기 (→ R2) |
  | 2 | Overlay Normal 허용 오차(°/dot) | [논의] | MMI "별도 정의" — Spec 수치 확정 필요 |
  | 3 | Section Slice 스크롤 NFR(ms) | [정보] | 개발실 리뷰 최대 리스크 — 구현 초기 벤치마크 |
  | 4 | Save Project Section 필드·I/O 경계 | [논의] | CW 팀 합의 (→ R3) |
  | 5 | Scout 명칭 변경 여부 | [정보] | 기획 7/10 검토 후 공유 예정 |
  | 6 | MMI.md vs PPT comments 드리프트 | [정보] | ESC·1점 더블클릭·proj Curve — Spec은 §4.2 우선 |

  - **차주 이월 후보:** R1(Spec 리뷰 일정) 미확정 · R2(B/L confirm) 지연 시 구현 범위 조정.

---

<!-- 다음 주부터: 위 「작성 규칙」템플릿 블록을 복사해 아래에 # M/D 주간회의 Agenda 를 추가 -->
