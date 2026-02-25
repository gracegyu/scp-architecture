# FMData 폴더 리포트 파일 검색 결과

담당자 전달 FMData 폴더 내 모든 파일을 확인하여, PoC-07 기준 E2 / E3 / E3RC / EzOrtho / CleverOne 리포트·템플릿을 구분한 결과입니다.

---

## 1. FMData 내 리포트·관련 파일 분류

| 경로 | 파일 수 | 형식 | 비고 |
|------|---------|------|------|
| **Report/Sub026021/*.rpt** | 40 | E2 v3.0 | `<Report Version="3.0">`, ItemBox Type=, XPercent (비율) |
| **Fixed/Report/Files/1/*.xml** | 41 | E3 **RC** Report v5.1 | `<Report Version="5.1.0" ARCHIVETYPE="Report">`, ItemBox, BoxPosition(mm) |
| **Fixed/ESReport/Report/1/*.rpt** | 40 | CleverOne | `<Report Version="5.1.0"\|"5.2.0" TemplateName=`, TextBox/ImageBox 직접 |
| **Chart/Sub026021/CH*.xml** | 11 | EzOrtho Treatment Chart | `<TreatmentChart>`, PageContent, Label/TextBox/ToothBox 등 |
| **Fixed/Template/*.xml** | 12 | E3 레거시 **템플릿** | `<Report>`, `<Page>`, `<Item>` + PositonX, Macro (리포트 아님) |
| **Fixed/Report/ReportTemplate/Default/*.xml** | 3 | 템플릿 (E3 RC 스타일) | ARCHIVETYPE="Template", ItemBox, BoxPosition |
| **Layout/Report/*.tpl** | 14 | CleverOne 스타일 템플릿 | .tpl |
| **Layout/Chart/Treatment/TreatmentChart.tpl** | 1 | EzOrtho 템플릿 | `<TreatmentChart>` 빈 구조 |
| **Files/Sub024061/*.bpt.xml** | 2 | 리포트 아님 | boost_serialization (column/row 포인트 데이터) |
| **Setting/*.xml** | 4 | 설정 | VTE2, EzOrtho, CleverOne 설정 |

---

## 2. E3 Report 샘플 여부

**PoC-07 기준 E3 종류**
- **E3 Report v4.0/v5.0**: 비율 좌표(XPercent 등), Template, Paper
- **E3 RC Report v5.1**: mm 좌표(BoxPosition), ItemBox, Version 5.1.0 → 현재 **Samples/E3RC**에 있음
- **E3 v1.x**: Base64 이미지 내장, Template, 다단계 변환

**FMData 검색 결과**
- **E3 Report v4/v5** (비율 좌표) 형식 파일: **없음**
- **E3 v1.x** (Base64 내장) 형식 파일: **없음**
- **E3 RC Report v5.1**: **Fixed/Report/Files/1/*.xml** 41개 → 이미 Samples/E3RC로 복사된 상태
- **E3 레거시**: **Fixed/Template/*.xml** 12개는 **템플릿**이며, 리포트 인스턴스가 아님 (Samples/E3에 있던 파일의 원본)

**결론**: FMData 안에는 **E3 Report (v4/v5 비율 또는 v1.x)** 형식의 **리포트 샘플이 없습니다**.  
담당자가 말한 “E3 리포트 샘플 포함”은 **E3 RC Report**(Fixed/Report/Files/1)를 의미한 것으로 보이며, 이는 이미 Samples/E3RC로 반영되어 있습니다.  
**E3 Report v4/v5** 또는 **E3 v1.x** 샘플이 필요하면 담당자에게 해당 형식의 리포트 파일 추가 전달을 요청하는 것이 좋습니다.

---

## 3. 요약

| 앱 | FMData 내 위치 | Samples 반영 |
|----|----------------|--------------|
| E2 | Report/Sub026021/*.rpt | Samples/E2 |
| E3 레거시 | Fixed/Template/*.xml (템플릿) | Templates/E3 (리포트 아님) |
| E3 RC | Fixed/Report/Files/1/*.xml | Samples/E3RC |
| EzOrtho | Chart/Sub026021/CH*.xml | Samples/EzOrtho |
| CleverOne | Fixed/ESReport/Report/1/*.rpt | Samples/CleverOne |

**E3 Report (v4/v5 또는 v1.x) 전용 리포트 샘플**: FMData에 없음.

---

**검색 일자**: 2026-01-23  
**참조**: PoC-07_Migration시스템설계_result.md
