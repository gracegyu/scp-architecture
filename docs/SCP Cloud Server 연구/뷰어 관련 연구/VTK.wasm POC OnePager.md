## Project Name

VTK.wasm 기반 3D CT Web 뷰어 POC

## Date

2025-09-29

## Submitter Info

작성자: Raymond

## Project Description

- VTK.wasm이 브라우저에서 의료용 3D CT 볼륨을 원활하게 렌더링/상호작용할 수 있는지 검증한다.
- 대상: DICOM CT 스택 → `vtkImageData` → 볼륨 렌더링(전이함수/카메라/조작), 슬라이스 탐색(옵션)
- 환경: 최신 크롬/엣지(데스크톱/모바일), 기본 WASM 번들 우선(필요 시 커스텀 번들 검토)

## Business and Marketing Justification

- 모바일 최적화된 3D 웹 뷰어 제공은 경쟁력과 사용자 만족도 향상에 핵심
- 클라이언트 사이드 렌더링 고도화로 서버 비용 절감 및 응답성 개선 기대
- VTK.js 대비 성능/기능 이점 확인 시 차세대 뷰어 기반 기술로 채택 가능성

## Risk Assessment

- 볼륨 렌더링 클래스가 번들에 포함되지 않았을 수 있음(기능 간극)
- 초기 로드/초기화 시간 및 메모리 사용량이 클 수 있음(특히 모바일)
- 생태계/문서 성숙도에 따른 통합 복잡도 및 유지보수 리스크
- 대응: 커스텀 빌드/하이브리드 전략(VTK.js 병행), 전처리(Rate10+binning), 단계적 범위 확장

## Resource and Scheduling Details

- 데이터: `CT20130424_213559_8924_40274191/` (약 196MB, 무압축 DICOM, 399개 슬라이스)
- 기간: 1주일 이내 (POC 검증 2~3일, 문서화 1~2일)
- 인력: 개발자 1명 (풀스택)

## Technical Description

- 목표/성공 기준

  - 핵심 목표: VTK.wasm으로 DICOM CT 3D 볼륨 렌더링이 가능한지 검증
  - 성공 기준: 브라우저에서 실제 CT 볼륨이 3D로 표시되는지 확인

- 작업 항목

  1. VTK.wasm 초기화 및 DICOM 파일 로딩
  2. VTK 볼륨 렌더링 클래스 존재 여부 확인
  3. 실제 3D 볼륨 렌더링 시도 및 결과 확인

- UI 범위

  - 최소 UI: 캔버스 1개 + 상태 표시
  - 기본 3D 상호작용 (마우스 조작)

## 개발 환경/도구

- UI 프레임워크: React 18 + TypeScript
- 패키지 매니저: pnpm
- 번들러: Vite
- 브라우저: Chrome
- VTK.wasm: `@kitware/vtk-wasm` npm 패키지

## POC 결과 및 결론

### 검증 결과

**VTK.wasm 3D 볼륨 렌더링: 부분적 가능 (제약 있음)**

1. **성공적인 검증 사항**:

   - **VTK 네임스페이스 생성**: `@kitware/vtk-wasm` npm 패키지의 `createNamespace()` 성공
   - **볼륨 렌더링 클래스 존재**: `vtkImageData`, `vtkVolumeMapper`, `vtkVolume` 등 모든 클래스 확인
   - **DICOM 데이터 로딩**: 399개 파일 (496x496x399, 98MB) 성공적 파싱
   - **VTK 객체 생성**: 브라우저에서 직접 VTK 객체 생성 성공
   - **3D 메시 렌더링**: PolyData 기반 3D 렌더링 완전 작동

2. **볼륨 렌더링 제약사항**:

   - **API 접근 제한**: `GetScalarPointer is not permitted`, `SetInputData is not permitted`
   - **데이터 설정 제한**: 볼륨 데이터를 ImageData에 설정하는 모든 방법 차단
   - **전이함수 설정 제한**: `AddPoint is not permitted` 오류

3. **기술적 아키텍처**:

   - **클라이언트 사이드 독립 실행**: 서버 없이 브라우저에서 완전 독립 동작
   - **공식 npm 패키지**: `@kitware/vtk-wasm` + CDN 번들 조합
   - **WebGL 기반 렌더링**: 브라우저의 WebGL을 통한 하드웨어 가속 3D 렌더링
   - **API 보안 제한**: 현재 번들은 읽기 전용 API만 제공

### 권장사항

**VTK.wasm 사용 가능**: 브라우저 기반 3D 의료 영상 뷰어 개발에 적용 가능

- **장점**:

  - 클라이언트 사이드 독립 실행 확인
  - VTK C++ 라이브러리의 완전한 기능 활용 가능
  - WebGL 하드웨어 가속을 통한 고성능 3D 렌더링
  - 공식 npm 패키지를 통한 안정적인 통합

- **고려사항**:

  - WebGL 환경 의존성 (대부분의 현대 브라우저에서 지원)
  - 초기 로딩 시간 (75MB WASM 번들)
  - VTK.js 대비 생태계 성숙도

- **결론**: **현재 VTK.js가 볼륨 렌더링에 더 적합**

### 최종 POC 결과 (2025-09-29)

**🎯 VTK.wasm 3D 볼륨 렌더링 검증 결과: 불가능 ❌**

## 1. 볼륨 렌더링 클래스 완전 존재 확인 ✅

**모든 필수 클래스가 VTK.wasm에 포함되어 있음:**

```javascript
사용 가능한 VTK 클래스들: [
  'vtkImageData',           // 볼륨 데이터 구조
  'vtkVolumeMapper',        // 볼륨 매퍼
  'vtkVolume',              // 볼륨 액터
  'vtkDataArray',           // 데이터 배열
  'vtkTypeUint16Array',     // 16bit 배열
  'vtkTypeFloat32Array',    // 32bit 배열
  'vtkColorTransferFunction', // 색상 전이함수
  'vtkPiecewiseFunction'    // 투명도 전이함수
]
```

## 2. DICOM 데이터 처리 완전 성공 ✅

**대용량 DICOM 데이터 로딩 및 파싱 성공:**

- ✅ **399개 DICOM 파일** 성공적 로딩
- ✅ **볼륨 크기**: 496 x 496 x 399 (약 98MB)
- ✅ **픽셀 데이터**: 각 파일 493,576 bytes → 492,032 bytes 추출
- ✅ **볼륨 데이터 생성**: Uint16Array(98,160,384) 완료

## 3. API 보안 제한으로 볼륨 렌더링 실패 ❌

### 3.1 데이터 설정 API 차단

```
vtkObjectManager: Invoker failed to call GetScalarPointer
Error: Call to vtkObjectBase::GetScalarPointer is not permitted.

vtkObjectManager: Invoker failed to call SetInputData
Error: Call to vtkObjectBase::SetInputData is not permitted.
```

### 3.2 전이함수 설정 API 차단

```
vtkObjectManager: Invoker failed to call AddPoint
Error: Call to vtkObjectBase::AddPoint is not permitted.
```

### 3.3 볼륨 매퍼 연결 API 차단

```
vtkObjectManager: Invoker failed to call SetMapper
Error: No suitable overload of 'vtkVolume::SetMapper' takes the specified arguments.
```

## 4. 볼륨 렌더링 불가능한 근본 원인

### 4.1 VTK.wasm 아키텍처 제약

**원격 객체 관리 방식:**

- VTK.wasm 객체들이 `vtkObjectManager`를 통해 **원격 관리**됨
- 클라이언트는 **객체 ID를 통한 간접 접근**만 가능
- 직접적인 메모리 접근 및 데이터 조작 **원천 차단**

### 4.2 API 보안 정책

**쓰기 작업 전면 금지:**

- `GetScalarPointer`, `SetInputData`, `AddPoint` 등 **핵심 API 차단**
- 볼륨 데이터 설정에 필수적인 **모든 쓰기 메서드 금지**
- 현재 번들은 **읽기 전용 API**만 허용

### 4.3 볼륨 렌더링 파이프라인 차단

**필수 단계별 차단 지점:**

1. **볼륨 데이터 설정**: `ImageData.setScalars()` 불가
2. **매퍼 연결**: `VolumeMapper.setInputData()` 불가
3. **전이함수 설정**: `ColorTransferFunction.addPoint()` 불가
4. **볼륨 액터 설정**: `Volume.setMapper()` 불가

## 5. 대안 구현 성공

**DICOM 기반 3D 메시 렌더링:**

- DICOM 중간 슬라이스 → 3D 높이맵 변환
- 62x62 그리드 메시 생성 (3,844개 포인트)
- HU 값 기반 높이 변환 및 3D 시각화
- 실시간 3D 상호작용 (회전, 줌, 패닝)

## 최종 결론

**VTK.wasm 3D 볼륨 렌더링: 기술적 불가능 (API 제한)**

**핵심 이유:**

1. **클래스 존재** vs **API 접근 차단**
2. **보안 정책**으로 볼륨 데이터 조작 전면 차단
3. **원격 객체 관리** 방식으로 직접 제어 불가

**권장사항**: **의료용 3D 볼륨 뷰어는 VTK.js 사용**

## 향후 VTK.wasm 모니터링 전략

### VTK.wasm의 잠재적 장점

**WebAssembly 성능 우위:**

- **JavaScript 대비 빠른 실행 속도**: 네이티브 코드에 가까운 성능
- **메모리 효율성**: 직접 메모리 관리로 가비지 컬렉션 오버헤드 없음
- **대용량 데이터 처리**: 의료 영상과 같은 대용량 볼륨 데이터에 유리
- **멀티스레딩 지원**: Worker를 통한 병렬 처리 가능

### 모니터링 방법 및 주기

**1. 정기적 기술 동향 모니터링**

- **주기**: 분기별 (3개월마다)
- **방법**:
  - VTK.wasm 공식 문서 및 릴리즈 노트 확인
  - Kitware 블로그 및 컨퍼런스 발표 모니터링
  - GitHub 리포지토리 활동 및 이슈 트래킹

**2. API 제한 해제 모니터링**

- **핵심 확인 사항**:
  - `SetInputData`, `GetScalarPointer` 등 핵심 API 접근 가능 여부
  - 볼륨 데이터 설정 및 전이함수 조작 가능 여부
  - 클라이언트 사이드 볼륨 렌더링 지원 여부

**3. 실무 검증 테스트**

- **방법**: 현재 POC 코드를 정기적으로 재실행
- **확인 포인트**:
  - 볼륨 렌더링 API 차단 해제 여부
  - 새로운 번들 버전의 기능 확장
  - 성능 개선 및 안정성 향상

**4. 대안 기술 동향 파악**

- **WebGPU + VTK**: 차세대 웹 그래픽 API 활용 가능성
- **Three.js + VTK.wasm**: 하이브리드 접근 방식
- **커스텀 VTK.wasm 빌드**: 필요한 API만 포함한 맞춤 번들

### 재검토 시점

**즉시 재검토가 필요한 신호:**

- VTK.wasm 메이저 버전 업데이트 (v10.x 등)
- Kitware에서 볼륨 렌더링 관련 공식 발표
- 의료 영상 분야 VTK.wasm 성공 사례 등장
- API 제한 정책 변경 공지

**권장 재검토 주기:**

- **단기**: 6개월마다 기술 동향 확인
- **중기**: 1년마다 실제 POC 재실행
- **장기**: 메이저 버전 출시 시 즉시 검증

**권장사항**: **의료용 3D 볼륨 뷰어는 현재 VTK.js 사용, VTK.wasm은 지속 모니터링**

- 참고 링크
  - Activities | VTK.wasm: https://kitware.github.io/vtk-wasm/
  - VTK.wasm from the JavaScript side: https://kitware.github.io/vtk-wasm/guide/js/
