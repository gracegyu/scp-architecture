# DICOM JPEG2000 압축 가이드

## 개요

402개의 비압축 DICOM 파일을 JPEG2000 형식으로 10배 손실 압축하는 방법들을 제공합니다.

## 방법 1: GDCM 사용 (추천)

GDCM은 DICOM 표준을 완벽하게 지원하는 가장 안전한 방법입니다.

### 설치

```bash
# macOS
brew install gdcm

# Ubuntu/Debian
sudo apt-get install gdcm-tools

# CentOS/RHEL
sudo yum install gdcm-tools
```

### 사용법

```bash
# 스크립트 실행
./scripts/compress_dicom_j2k.sh
```

### 특징

- DICOM 메타데이터 완벽 보존
- 의료용 표준 준수
- 안정적인 처리
- 배치 처리 지원

## 방법 2: Python (pydicom + Pillow)

Python 환경에서 세밀한 제어가 필요한 경우 사용합니다.

### 설치

```bash
pip install pydicom pillow numpy
```

### 사용법

```bash
# 기본 경로로 실행
python3 scripts/compress_dicom_j2k.py

# 커스텀 경로로 실행
python3 scripts/compress_dicom_j2k.py /path/to/input /path/to/output
```

### 특징

- 세밀한 압축 제어
- 이미지 전처리 가능
- 배치 처리 지원
- 진행상황 표시

## 방법 3: dcmtk 사용

dcmtk는 DICOM 처리의 표준 도구입니다.

### 설치

```bash
# macOS
brew install dcmtk

# Ubuntu/Debian
sudo apt-get install dcmtk
```

### 사용법

```bash
# 단일 파일 압축
dcmcjpeg +oj +CJ input.dcm output.dcm

# 배치 처리 스크립트
for file in *.dcm; do
    dcmcjpeg +oj +CJ "$file" "compressed_$file"
done
```

## 방법 4: ImageMagick (단순한 경우)

이미지만 압축하고 DICOM 메타데이터가 중요하지 않은 경우 사용합니다.

### 설치

```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
sudo apt-get install imagemagick
```

### 사용법

```bash
# 단일 파일
convert input.dcm -quality 10 -define jpeg:q-table=0 output.jp2

# 배치 처리
for file in *.dcm; do
    convert "$file" -quality 10 output/"${file%.dcm}.jp2"
done
```

## 압축률 조정

### 품질 설정 가이드

- `quality=1-5`: 20-50배 압축 (매우 높은 압축률, 낮은 품질)
- `quality=6-15`: 10-20배 압축 (높은 압축률, 보통 품질) ⭐ **권장**
- `quality=16-30`: 5-10배 압축 (보통 압축률, 좋은 품질)
- `quality=31-50`: 2-5배 압축 (낮은 압축률, 높은 품질)

### 10배 압축을 위한 최적 설정

```bash
# GDCM
gdcmconv --j2k --lossy --quality 10 input.dcm output.dcm

# Python
quality=10  # 스크립트 내에서 조정

# dcmtk
dcmcjpeg +oj +CJ -q 10 input.dcm output.dcm
```

## 결과 확인

### 압축률 계산

```bash
# 원본 크기
du -sh examples/host-app/public/dummy/CT20130424_213559_8924_40274191

# 압축 후 크기
du -sh examples/host-app/public/dummy/CT20130424_213559_8924_40274191_compressed

# 개별 파일 비교
ls -lh original.dcm compressed.dcm
```

### DICOM 뷰어로 확인

압축된 파일이 올바르게 열리는지 확인:

- OHIF Viewer
- RadiAnt
- Horos (macOS)
- 3D Slicer

## 주의사항

1. **백업 필수**: 원본 파일을 반드시 백업하세요
2. **품질 검증**: 압축 후 의료진이 품질을 확인해야 합니다
3. **표준 준수**: DICOM 표준을 준수하는 도구를 사용하세요
4. **메타데이터**: 중요한 DICOM 메타데이터가 보존되는지 확인하세요

## 성능 비교

| 방법        | 압축률     | 속도       | 품질 보존  | DICOM 호환성 |
| ----------- | ---------- | ---------- | ---------- | ------------ |
| GDCM        | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐   |
| Python      | ⭐⭐⭐⭐   | ⭐⭐⭐     | ⭐⭐⭐⭐   | ⭐⭐⭐⭐     |
| dcmtk       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐   |
| ImageMagick | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐         |

## 추천 워크플로우

1. **소량 테스트**: 먼저 5-10개 파일로 테스트
2. **품질 확인**: 의료진이 압축 품질 검토
3. **설정 조정**: 필요시 압축률 조정
4. **전체 처리**: 전체 402개 파일 처리
5. **결과 검증**: 모든 파일이 올바르게 압축되었는지 확인

## 예상 결과

- **원본 크기**: 약 194MB (402 × 482KB)
- **압축 후 크기**: 약 19.4MB (10배 압축 시)
- **처리 시간**: 5-15분 (방법에 따라)
- **품질**: 진단에 적합한 수준 유지
