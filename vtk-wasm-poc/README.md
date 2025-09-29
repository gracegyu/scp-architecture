# VTK.wasm POC (React + TypeScript + Vite)

본 POC는 브라우저에서 VTK.wasm을 이용해 3D 뷰어 렌더링 가능성을 검증하기 위한 최소 구현입니다.

## 요구사항

- Node 20.19+ (또는 22.12+), pnpm
- macOS 환경: nvm 자동 로드 설정 권장

## 설치/실행

```bash
pnpm install
pnpm dev
```

- Node 오류 시:

```bash
nvm install 20.19.3
nvm alias default 20.19.3
node -v
```

## 자산/데이터

- `/public/dummy` 심볼릭 링크로 대용량 자산을 개발 중에만 서빙
- 허용 경로는 `vite.config.ts`의 `server.fs.allow`에서 관리

## trame vs 우리 접근 방식

**trame**: Python 기반 웹 애플리케이션 프레임워크 (Python 백엔드 + Vue.js 프론트엔드) **우리 POC**: 순수 JavaScript/React 클라이언트 사이드 렌더링

**trame-vtklocal 활용**: trame용이지만 VTK.wasm 빌드 도구와 JS 프록시가 포함된 번들을 생성하므로 우리가 활용

## VTK.wasm 번들 종류

- 코어 번들(`vtkWebAssembly*.mjs/wasm`): 런타임 로더. `vtk` 네임스페이스 없음(렌더 불가)
- trame 번들(렌더 프록시 포함): `vtk.vtkRenderer()` 등 사용 가능
  - 참고: [VTK.wasm JS 가이드](https://kitware.github.io/vtk-wasm/guide/js/)

## VTK.wasm 번들 사용

### 기존 trame 번들 활용

이미 `/public/vtk-wasm/wasm32/` 디렉토리에 trame용 VTK.wasm 번들이 포함되어 있습니다:

- `vtkWebAssemblyAsync.mjs` - trame 번들 (vtk 네임스페이스 포함)
- `vtkWebAssemblyAsync.wasm` - WASM 바이너리

### 번들 확인

```bash
ls -la vtk-wasm-poc/public/vtk-wasm/wasm32/
# vtkWebAssemblyAsync.mjs (260KB) - JS 프록시 포함
# vtkWebAssemblyAsync.wasm (69MB) - WASM 바이너리
```

## 개발 메모

- public의 `.mjs`는 소스 import 불가 → fetch→Blob URL→dynamic import 적용(이미 구현)
- 포트 충돌 시 `pnpm dev --port 517x`

## 문제 해결

### 런타임 오류

**"vtk 네임스페이스 미발견" 오류**:

- 기존 trame 번들(`vtkWebAssemblyAsync.mjs`) 사용 확인
- 브라우저 개발자 도구에서 로딩 오류 확인

**메모리 부족 오류**:

- 브라우저 개발자 도구에서 메모리 사용량 모니터링
- 대용량 CT 대신 소형 데이터셋으로 테스트

**WASM 로딩 실패**:

- Vite 개발 서버가 WASM 파일을 올바르게 서빙하는지 확인
- 네트워크 탭에서 `.mjs`, `.wasm` 파일 로딩 상태 확인

## 진행 체크리스트

- [x] wasm32 로더 초기화
- [x] 기존 trame 번들 확인 및 활용
- [x] trame 번들 연결 → `vtk` 네임스페이스 확인
- [x] 기본 3D 장면 렌더링 (쿼드 메시)
- [ ] 3D 볼륨 렌더링 → FPS/메모리 측정
- [ ] DICOM 스택 로더(소형 세트)

## POC 결과 (2025-09-29)

**VTK.wasm 클라이언트 사이드 3D 렌더링: 불가능**

### 검증 완료 사항

- ✅ VTK.wasm 번들 로딩 및 초기화
- ✅ `vtkStandaloneSession` 생성 및 분석
- ✅ ClassHandle 기반 API 구조 확인
- ❌ 독립적인 클라이언트 사이드 VTK 팩토리 함수 접근 실패

### 기술적 결론

현재 VTK.wasm은 **서버-클라이언트 아키텍처** (trame 스타일):

- `vtkObjectManager` 기반 서버 측 객체 관리
- 클라이언트는 객체 ID를 통한 원격 호출만 지원
- Python 백엔드 없이는 VTK 객체 생성/렌더링 불가능

### 권장사항

**VTK.js 사용 권장**: 브라우저 기반 3D 의료 영상 뷰어 개발에 적합

## 참고 링크

- VTK.wasm JS 가이드: https://kitware.github.io/vtk-wasm/guide/js/
- VTK.wasm 활동: https://kitware.github.io/vtk-wasm/
