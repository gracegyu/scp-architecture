# Samples 폴더 검산 보고서

PoC-07(Migration 시스템 설계), PoC-06(통합 Element 스키마 설계)에 정의된 제품별 리포트 포맷과 Samples 하위 폴더(E2, E3RC, EzOrtho, CleverOne) 내 파일이 일치하는지 검산한 결과입니다. E3 Report(레거시) 리포트 샘플은 없음.

---

## 1. 검산 기준 (PoC-07 / PoC-06)

| App | PoC-07 포맷 요약 | 좌표 단위 | 식별 핵심 |
|-----|------------------|-----------|------------|
| **E2** | v3.0, Template 부재, Paper·ImageBox·TextBox 중심 | 비율값 (0~1, XPercent/WidthPercent) | `<Report Version="3.0">`, `<Page XPercent= YPercent=>`, `<ItemBox Type="ImageBox"\|"TextBox"\|...>` |
| **E3** | v1.x 레거시 (참고) | 픽셀/고정 해상도 | Samples에 리포트 샘플 없음. 동일 형식 템플릿은 Templates/E3 참고. |
| **E3RC** | E3 RC Report v5.1, ItemBox(Text/Image), CapturedImageInfo | mm (1자리→3자리) | `<Report Version="5.1.0">`, `<ItemBox>`, `<BoxType>Image\|Text`, `<BoxPosition><X>`, `<Paper>` 자식요소 |
| **EzOrtho** | v1.0, Treatment Chart, Label·TextBox·ImageBox·ToothBox·TreatmentCategory·Block | mm | `<TreatmentChart>`, `<PaperSetting>`, `<Header>`/`<Footer>`/`<PageContent>`, `<Label>`/`<TextBox>`/`<ImageBox>`/`<ToothBox>`/`<TreatmentCategory>`/`<Annotations>` |
| **CleverOne** | v5.1.0, TextBox/ImageBox/ToothBox/Annotations/Groups, Template | %(비율, 실제 샘플 기준) | `<Report Version="5.1.0"\|"5.2.0" TemplateName= ARCHIVETYPE=`, `<Paper PaperSize=`, `<TextBox BoxID=`, `<ImageBox BoxID=`, `<Position X="6.950%"`, `<Size Width="81%"`, `<Annotations>`/`<Groups>` |

---

## 2. E2 (Samples/E2)

**파일 수**: 40개 (모두 `.rpt`)

**검산 결과**: 일치

| 검사 항목 | PoC-07 정의 | 실제 샘플 |
|-----------|-------------|-----------|
| 루트 | Report, Template 부재 | `<Report Version="3.0">` (Template 없음) |
| 페이지 | 용지/비율 | `<Page IncludeImageInfo="2" XPercent="210" YPercent="297" PageNumber="0">` (또는 300/240 등) |
| 요소 | ImageBox, TextBox (→ Cloud imageBox, textBox) | `<ItemBox Type="ImageBox" ... XPercent="0.1" WidthPercent="0.8">`, `<ItemBox Type="HeaderDateBox" ...>`, `<ItemBox Type="TextBox" ...>` 등 |
| 좌표 | 비율값 (0~1) | XPercent, YPercent, WidthPercent, HeightPercent 사용 |

**비고**: PoC-07 매핑 테이블의 "ImageBox / TextBox"는 Cloud Element명이며, E2 소스는 `ItemBox Type="ImageBox"` 등으로 동일 의미. Header*Box, Footer*Box는 레이아웃용으로 E2 포맷 내 정상.

---

## 3. E3 (Samples/E3)

**파일 수**: 0개 (리포트 샘플 없음)

**E3 Report vs E3RC 관계 (기존 문서 스펙 기준)**  
- e3_report_v5.0_srs.md: E3의 Report 모듈(Report Tab), v1.x~v4.0/v5.0 포맷.  
- e3_rcreport_v5.1_srs.md: "RC Report 모듈은 기존 E3 Report 모듈의 편집 기능을 강화하고 Template 편집·관리 기능을 추가한 모듈"이며, "E3 v5.0 이하에서 제공했던 Report Tab은 **더 이상 제공하지 않는다**." v5.0 이하에서 작성한 Report 파일은 v5.1에서 Open 시 v5.1 포맷으로 Migration됨. v5.1에서 작성한 Report는 v5.0에서 Open 불가.  
- **정리**: E3 최신 버전(v5.1 이상)에서는 **생성되는 리포트는 RC Report(v5.1) 포맷만 존재**함. E3 Report(v4.0/v5.0) 포맷은 v5.0 이하에서만 생성되며, v5.1에서는 Open 시 RC 포맷으로 마이그레이션되므로 두 포맷이 동시에 “새로 생성”되는 구조는 아님. 다만 현장에 v5.0 이하로 저장된 E3 Report 파일이 레거시로 남아 있을 수 있어, 마이그레이션 경로(1.x→4.x→5.1→Cloud) 검증을 위해 해당 포맷 샘플이 필요함.

**비고**: E3 Report(레거시, v1.x~v5.0) 포맷의 리포트 파일은 Samples에 없음. FMData 등 담당자 전달 자료에도 E3 Report v4/v5 또는 v1.x 형식 리포트는 포함되어 있지 않았고, 동일 구조의 레이아웃 파일은 템플릿(Templates/E3)으로만 존재함. E3 계열 리포트는 현재 E3RC(Samples/E3RC)만 보유.  
**추가 확보 권장**: PoC-07의 "E3 v1.x → v5.1 → Cloud" 마이그레이션 경로를 검증하려면 E3 레거시 리포트 샘플이 필요함. E3RC만으로는 레거시 인풋에 대한 변환·매핑 검증이 불가하므로, v5.0 이하 제품에서 저장된 E3 Report 파일 샘플 확보를 담당자에게 요청 권장함.

---

## 4. E3RC (Samples/E3RC)

**파일 수**: 41개 (모두 `20260224_*.xml`)

**검산 결과**: 일치 (E3 RC Report v5.1)

| 검사 항목 | PoC-07 정의 | 실제 샘플 |
|-----------|-------------|-----------|
| 루트 | Report Version 5.1.0, ARCHIVETYPE="Report" | `<Report ARCHIVETYPE="Report" Version="5.1.0" TemplateName="...">` |
| Paper | PaperSize, Orientation, Margin | `<Paper>` 하위 `<PaperSize>`, `<Orientation>`, `<Margin><Left>`, `<Right>` 등 |
| 요소 | ItemBox(Text), ItemBox(Image), CapturedImageInfo | `<ItemBox>` → `<BoxType>Image</BoxType>` / `<BoxType>Text</BoxType>`, `<BoxPosition><X>`, `<BoxSize><BoxWidth>`, `<CapturedImgInfo>`, `<ImageAcqInfo>` |
| 좌표 | mm (1자리 → 3자리 확장) | `<X>45.5664</X>`, `<Y>53.6216</Y>` (mm) |

---

## 5. EzOrtho (Samples/EzOrtho)

**파일 수**: 11개 (모두 `CH*.xml`)

**검산 결과**: 일치

| 검사 항목 | PoC-07 정의 | 실제 샘플 |
|-----------|-------------|-----------|
| 루트 | Treatment Chart, Chart 구조 | `<TreatmentChart Name="" Version="" Locale="ko_KR">` |
| 용지/헤더/푸터 | PaperSetting, Header, Footer | `<PaperSetting PaperSize="A4" ...>`, `<Header>`, `<Footer>`, 푸터에 "Printed By EzOrtho" |
| 본문 | Label, TextBox, ImageBox, ToothBox, TreatmentCategory, Annotations | `<PageContent>` 내 `<Label>`, `<TextBox>`, `<ImageBox>`, `<ToothBox>`, `<TreatmentCategory>`, `<Annotations/>` |
| 좌표 | mm | Left, Top, Width, Height (숫자 또는 소수) |

PoC-07의 EzOrtho Element(Label, TextBox, ImageBox, ToothBox, TreatmentCategory, Block) 및 Chart 구조와 일치.

---

## 6. CleverOne (Samples/CleverOne)

**파일 수**: 41개 (40개 `1_*.rpt`, 1개 `Confidential_CleverOne_Report_Example.xml`)

**검산 결과**: 일치

| 검사 항목 | PoC-07 정의 | 실제 샘플 |
|-----------|-------------|-----------|
| 루트 | Report Version 5.1.0/5.2.0, TemplateName, ARCHIVETYPE | `<Report TemplateName="RPT_Frame2x1L" Version="5.2.0" ARCHIVETYPE="Template">` 또는 `Version="5.1.0" ARCHIVETYPE="Report"` |
| Paper | PaperSize, Margin 속성형 | `<Paper PaperSize="A4" Orientation="Portrait">`, `<Margin Top="10" Bottom="10" Left="10" Right="10"/>` |
| 요소 | TextBox, ImageBox, ToothBox, Annotations, Groups | `<TextBox BoxID="30" ...>`, `<ImageBox BoxID="29" ... BoxType="Single">`, `<Position X="6.950%" Y="50.051%"/>`, `<Size Width="81%" Height="35%"/>`, `<Annotations/>`, `<Groups/>` |
| 좌표 | %(비율, 실제 샘플 기준) | Position X/Y, Size Width/Height에 % 단위 (예: 1_40.rpt). 기존 스펙 문서의 mm 기술과 상이. |

PoC-07 "CleverOne Element: TextBox, ImageBox, ToothBox, Annotation, Groups, Template" 및 BoxType(Single/Multi/Reference) 설명과 일치. 실제 리포트 파일(1_*.rpt)은 Position/Size가 % 단위로 저장됨.

---

## 7. 요약

| 폴더 | 파일 수 | PoC-07/06 포맷 일치 | 비고 |
|------|----------|----------------------|------|
| E2 | 40 | 예 | ItemBox Type + XPercent 구조 |
| E3 | 0 | - | 리포트 샘플 없음. v1.x→v5.1→Cloud 검증을 위해 추가 확보 권장 (템플릿은 Templates/E3) |
| E3RC | 41 | 예 | E3 RC Report v5.1 (20260224_*.xml) |
| EzOrtho | 11 | 예 | TreatmentChart, PageContent 요소 |
| CleverOne | 41 | 예 | Report 5.1/5.2, TextBox/ImageBox 직접 사용 |

**결론**: Samples/E2, E3RC, EzOrtho, CleverOne에 있는 리포트 파일은 PoC-07·PoC-06에서 정의한 해당 포맷과 일치합니다. E3 Report(레거시) 리포트 샘플은 없으며, E3 계열은 E3RC만 보유합니다.

---

**검산 일자**: 2026-01-23  
**참조 문서**: PoC-07_Migration시스템설계_result.md, PoC-06_통합Element스키마설계_result.md
