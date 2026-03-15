# Samples vs 스펙 문서 검토

확보된 Samples(E2, E3RC, EzOrtho, CleverOne)와 PoC-02, PoC-03, SCP Cloud Report PoC 설계 문서의 기술을 대조한 결과입니다.

**요약 (5줄)**  
E2·E3RC·CleverOne은 문서와 일치. EzOrtho만 PoC-02에 "주석에 unit : mm 명시"로 되어 있었으나 확보 샘플 11건에는 해당 주석이 없고, 좌표는 숫자형(mm 해석)으로 문제 없음. PoC-02 EzOrtho 문구는 "숫자형 좌표, mm 해석"으로 완화 권장(이미 반영됨).

---

## 1. 검토 범위

| 대상 | 내용 |
|------|------|
| Samples | E2(40), E3RC(41), EzOrtho(11), CleverOne(41) |
| 문서 | PoC-02_좌표값단위시스템_result.md, PoC-03_DPI및렌더링전략결정_result.md, SCP Cloud Report PoC 설계.md, Samples_검산보고.md |

---

## 2. 제품별 검토 결과

### 2.1 E2 (Samples/E2)

| 문서 기술 | 실제 샘플 | 오차 |
|-----------|------------|------|
| Report Version="3.0", Template 부재 | 일치 (`<Report Version="3.0">`, Template 없음) | 없음 |
| 좌표: 비율값 (0~1), XPercent/WidthPercent | ItemBox: XPercent="0.1", YPercent="0.15", WidthPercent="0.8" 등 0~1 범위 | 없음 |
| Page: 용지/비율 | Page: XPercent="210" YPercent="297" (용지 치수 210×297), ItemBox는 비율 | 없음 |

**정리**: 문서와 일치. Page의 XPercent/YPercent는 용지 크기(210×297 등), ItemBox는 0~1 비율값.

---

### 2.2 E3RC (Samples/E3RC)

| 문서 기술 | 실제 샘플 | 오차 |
|-----------|------------|------|
| Report Version="5.1.0", ARCHIVETYPE="Report" | 일치 | 없음 |
| 좌표: mm (1자리→3자리 확장) | BoxPosition `<X>45.5664</X>`, `<Y>53.6216</Y>`, BoxSize 소수 포함 | 없음 |
| Paper, ItemBox, BoxType, CapturedImgInfo 등 | 구조 일치 | 없음 |

**정리**: 문서와 일치. 좌표는 단위 미명시이나 숫자형으로 mm 사용으로 해석 가능.

---

### 2.3 EzOrtho (Samples/EzOrtho)

| 문서 기술 | 실제 샘플 | 오차 |
|-----------|------------|------|
| TreatmentChart, PaperSetting, Header/Footer, PageContent | 구조 일치 | 없음 |
| 좌표: mm | Left, Top, Width, Height 숫자형 (예: 5, 99.002, 190, 2.442, 47.679) | 없음 |
| PoC-02: "주석에 `<!-- unit : mm -->` 명시" | **확보 샘플 전체에서 해당 주석 없음** | **있음** |

**정리**: 좌표는 숫자만 있으며 mm로 해석하는 데 무리 없음. 다만 PoC-02에서 "샘플 파일 확인 결과 주석에 unit : mm 명시"라고 한 부분은 **현재 확보한 11개 샘플에는 해당 주석이 없음**. 스펙 또는 다른 버전 샘플 기준일 수 있으므로, 문서에서는 "실제 파일 구조 확인 결과 숫자형 좌표 사용(mm 해석)" 정도로 완화하는 것을 권장.

---

### 2.4 CleverOne (Samples/CleverOne)

| 문서 기술 | 실제 샘플 | 오차 |
|-----------|------------|------|
| 실제 샘플 기준 %(비율) | 1_1.rpt, 1_40.rpt 등: `<Position X="5%" Y="49%"/>`, `<Size Width="81%" Height="35%"/>` | 없음 |
| 스펙 문서와 상이 | Confidential_CleverOne_Report_Example.xml: `X="10.5" Y="20.5"` (숫자만, % 없음) | 없음 |

**정리**: 문서와 일치. 실제 리포트(1_*.rpt)는 % 단위, Example.xml은 스펙 예제 형태(숫자만). 문서가 "실제 샘플 기준 %"로 정리된 것은 확보 샘플과 일치.

---

## 3. PoC-03, SCP 설계 문서

- **PoC-03**: 제품별 샘플 구조를 기술하지 않고, mm 좌표계·DPI·pt 등 통합 전략만 다룸. Samples와 직접 대조할 내용 없음. **오차 없음**.
- **SCP Cloud Report PoC 설계**: 제품별 특징 요약만 있음. E2 비율값, E3/RC mm, EzOrtho mm, CleverOne % 기술은 위 검토 결과와 일치. **오차 없음** (EzOrtho의 unit : mm 주석은 설계 문서에 없음).

---

## 4. 요약 및 권장 사항

| 제품 | 일치 여부 | 비고 |
|------|-----------|------|
| E2 | 일치 | - |
| E3RC | 일치 | - |
| EzOrtho | 대체로 일치 | PoC-02의 "주석에 unit : mm 명시"만 확보 샘플에 없음. 문구 완화 권장. |
| CleverOne | 일치 | - |

**권장**: PoC-02에서 EzOrtho 관련 "스펙 문서 및 샘플 파일 확인 결과: 주석에 `<!-- unit : mm -->` 명시" 문구를, 확보 샘플에는 해당 주석이 없으므로 "실제 파일 구조 확인 결과 숫자형 좌표 사용(mm 단위로 해석)" 등으로 수정하는 것을 권장합니다.

---

**검토 일자**: 2026-01-23  
**참조**: Samples_검산보고.md, PoC-02, PoC-03, SCP Cloud Report PoC 설계.md
