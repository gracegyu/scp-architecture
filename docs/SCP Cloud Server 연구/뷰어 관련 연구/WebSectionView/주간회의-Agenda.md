# Web Section View / Cloud Web Viewer v1.3.2 Section 모듈 — 주간회의 Agenda

> **용도:** Section Layout(Section 모듈) 개발·Spec·인계 진행을 주간 회의에서 공유·결정할 때 사용한다.  
> **참고 형식:** [VT API Gateway 주간회의 Agenda](../../VT_API_Gateway/08.VT_API_Gateway/주간회의-Agenda.md)  
> **정본 문서:** `Cloud Web Viewer v1.3.2/` — [OnePager Spec](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-Spec-v1.3.2-OnePager.md) · [개발계획](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-개발계획.md) · [구현계획서(IP)](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-ImplementationPlan.md) · [작업 가이드](./Cloud%20Web%20Viewer%20v1.3.2/Claude%20Code%20작업%20가이드.md)  
> **공유(리뷰):** [OnePager — VKS](https://vks.vatech.com/spaces/ESDEVELOPER/pages/320005969/Cloud+Web+Viewer+v1.3.2+%E2%80%94+Section+Module+%EA%B0%9C%EB%B0%9C+OnePager)

---

## 작성 규칙 (템플릿)

매주 **회의 직전**에 아래 블록을 **파일 맨 아래에 추가**한다. 이전 주 스냅샷은 **삭제하지 않고 보존**(GW Agenda와 동일).

### 주차 블록 구조

| 섹션               | 용도                                             |
| ------------------ | ------------------------------------------------ |
| **이번 주 진행**   | 지난 주 이후 완료·진행 중 작업 (불릿)            |
| **논의 사항**      | 결정·확인이 필요한 항목 — `R1`, `R2` …           |
| **공유 사항**      | 결정 아님 — 진행·일정·리스크 공유 — `S1`, `S2` … |
| **이월 논의 사항** | 미결 표 — `#` · 항목 · 타입 · 상태               |

### 타입 (논의·이월 표)

| 타입   | 의미                          |
| ------ | ----------------------------- |
| [확정] | 기결정 공식 확정·승인         |
| [논의] | 방향·범위 결정 필요           |
| [정보] | 추가 입력·자료·담당자 확보    |
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

  | #   | 항목 | 타입   | 상태 |
  | --- | ---- | ------ | ---- |
  | 1   | …    | [논의] | …    |
  - **차주 이월 후보:** R1 미확정 시 다음 주 이월.
```

### 관련 링크 (회의 전 확인)

| 항목                      | 위치                                                                         |
| ------------------------- | ---------------------------------------------------------------------------- |
| MMI v0.9.1                | `Cloud Web Viewer v1.3.2/기획·요구사항/MMI/MMI.md`                           |
| UI 시각 정본              | `.../기획·요구사항/MMI/media/image23.png`                                    |
| 기획 답변                 | [PLAN-1287.md](./Cloud%20Web%20Viewer%20v1.3.2/기획·요구사항/PLAN-1287.md)   |
| 개발실 리뷰               | [MMI\_개발실리뷰.md](./Cloud%20Web%20Viewer%20v1.3.2/검토/MMI_개발실리뷰.md) |
| PoC 결과                  | `PoC/Phase1/` … `Phase5/`                                                    |
| 구현 레포                 | `scp-section-poc`                                                            |
| Cloud Web Viewer(CW) 참조 | `cloudwebviewer`                                                             |
| EzCloud Test (MPR·툴바)   | https://container.test.ezcloud.ezcld.net/                                    |

---

# Cloud Web Viewer v1.3.2 Section 모듈 — 7/16 주간회의 Agenda

> **Spec 완성·VKS 리뷰 요청 시점 스냅샷.** OnePager v1.5 완성 후 공유·리뷰 요청, 구현 착수 직전.

- 이번 주 진행 (7/10 이후 · 회의 전까지 갱신)
  - **OnePager Spec v1.5 완성** — MMI 1.1~1.14 전 기능 매핑·모드표, 접목 정합(환경·인터페이스·common/core·Toolbar 통신), Overlay·Draw curve·Save·NFR. spec-reviewer 독립 검토 반영
  - **VKS 등록·리뷰 요청** — [OnePager (VKS)](https://vks.vatech.com/spaces/ESDEVELOPER/pages/320005969/Cloud+Web+Viewer+v1.3.2+%E2%80%94+Section+Module+%EA%B0%9C%EB%B0%9C+OnePager) (→ S1)
  - **B/L 자동 판정 확정** (기획 회신 7/13) — P1→P2 선분에서 CT 단면 중심 C쪽=L, **최초 2점 1회 고정**, 이후 편집 무영향·변경은 수동 L/B Switching (구 동적 반전 초안 폐기)
  - **접목 방식 확정** — CW vtk 미접목, Section(WebGL, PoC 확장)만 구현 + CW가 embed. 조사: `@cloudwebviewer/core`는 Module Federation 앱이라 Toolbar 직접 import 불가 → `core-types`만 link, 데모는 CW-스타일 stub
  - **개발계획 v0.9 현행화 · 구현계획서(IP) v0.1 작성** — IP 표준 8섹션·24 Task(완료 체크박스)·의존성 DAG. ip-reviewer 점검(잔여 BLOCKER 1건 = 문서 커밋 후 SHA 동결)
  - cloudwebviewer 실조사 — Module Federation·prj 스키마(Curve/Section/Pano 필드 기존재)·버전 정본(pnpm 9.15.9·React 18.2·Vite 5·MUI 5.15) 확인

- 논의 사항
  - **R1. Spec 리뷰 데드라인·참석·착수 gate** — OnePager VKS 등록 완료. **결정 요청:** 리뷰 회신 기한, 필수 참석(기획 Jessi·CW Viewer 담당), 리뷰-구현 착수 병행 여부.
    - **성격:** [논의]

  - **R2. Save prj — CW 스키마 필드 확인** — 방향 확정(CW prj XML 호환 + 개발 중 브라우저 임시저장, OnePager §7). **CW팀 확인 요청:** `vtkjs-wrapper/…/projectFile.ts`의 Section/Curve/Pano 필드 실제 구조·매핑 가능성.
    - **성격:** [논의] · 담당: CW Viewer

  - **R3. 구현 착수 승인** — 문서 3종 커밋 → IP §2 SHA 동결 → IP v1.0 baseline 후 P0(환경 정렬)부터 착수. **결정 요청:** 커밋·착수 시점.
    - **성격:** [논의] · 담당: Raymond + PL

- 공유 사항
  - **S1. OnePager VKS 등록·리뷰 요청** — [Cloud Web Viewer v1.3.2 — Section Module 개발 OnePager (VKS)](https://vks.vatech.com/spaces/ESDEVELOPER/pages/320005969/Cloud+Web+Viewer+v1.3.2+%E2%80%94+Section+Module+%EA%B0%9C%EB%B0%9C+OnePager). 기획·CW Viewer 팀 리뷰 요청.
  - **S2. 현재 단계** — `PoC 완료 → Spec 완성·VKS 리뷰 요청 [지금] → (병행) 환경 정렬·구현 착수 → 인계 → CW embed·접목`
  - **S3. 문서 상태** — OnePager **v1.5** / 개발계획 **v0.9** / IP **v0.1**(3종 미커밋 — 커밋 시 IP SHA 동결·v1.0 baseline).
  - **S4. 일정** — **구현 7/13부터 2주**(환경 정렬·Slice 스크롤 벤치마크 포함), 이후 **CW 팀 접목**. Slice 스크롤 성능은 구현 중 벤치마크(별도 PoC 아님). Raymond **VT API Gateway 병행(부분투입)** — 주간 갱신.

    ```mermaid
    gantt
        title Section 모듈 — 잠정 일정 (7/16 스냅샷)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:2px,stroke:#d33,opacity:0.5

        section 문서·Spec
        OnePager Spec v1.5 완성 + VKS 등록   :done, spec, 2026-07-10, 4d
        Spec 리뷰 (기획 + CW)                :active, specrv, 2026-07-13, 7d

        section 구현 (scp-section-poc)
        모듈 구현 (Section View · 환경 정렬 · Slice 벤치마크 포함)  :active, impl, 2026-07-13, 14d

        section 접목 (CW 팀)
        인계 → CW Viewer embed·접목           :integ, after impl, 14d
    ```

  - **S5. Known gaps** — Arrow 툴 CW `InteractionType` 미포함(접목 시 core 반영) · Scout=MPR Axial 접목 교체 전제 · Overlay Normal 허용 오차 5° 튜닝 · Slice 스크롤 NFR 벤치마크.

- 이월 논의 사항 (7/16 기준 · 미결)

  | #   | 항목                            | 타입   | 상태                                         |
  | --- | ------------------------------- | ------ | -------------------------------------------- |
  | 1   | Overlay Normal 허용 오차(°)     | [정보] | 초기값 5° 제안 — 구현 초기 튜닝 후 고정      |
  | 2   | Section Slice 스크롤 NFR(ms)    | [정보] | 개발실 리뷰 최대 리스크 — 구현 초기 벤치마크 |
  | 3   | Save Project — CW prj 필드 확인 | [논의] | 방향 확정, CW 팀 스키마 확인 (→ R2)          |
  | 4   | 문서 커밋·IP baseline·착수      | [선결] | 3종 커밋→SHA 동결→IP v1.0 (→ R3)             |
  - **확정·정리됨 (이번 주):** B/L 자동 판정(확정, OnePager §5) · 접목 방식(D1 — CW vtk 미접목·WebGL embed) · 개발 레포 방안 1 · Scout 명칭 유지(D8) · MMI drift(OnePager 반영).
  - **차주 이월 후보:** R1(리뷰 기한) 미확정 · R2(CW 필드) 회신 지연 시 Save 구현 순연.

---

<!-- 다음 주부터: 위 「작성 규칙」템플릿 블록을 복사해 아래에 # M/D 주간회의 Agenda 를 추가 -->
