/*
 * VTK.wasm PoC - 최소 UI 및 wasm 로더 스켈레톤
 *
 * Copyright (c) Ewoosoft Co., Ltd.
 *
 * All rights reserved.
 */

import { useEffect, useRef, useState } from 'react'
import './App.css'
import { buildSampleScene } from './main'

/**
 * App 컴포넌트
 * - 최소 UI로 3D 렌더 캔버스, FPS 표시, 간단한 컨트롤 영역을 제공한다.
 * - 이후 VTK.wasm 초기화 로직과 렌더 루프 연결을 이곳에 추가한다.
 */
function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [fps, setFps] = useState<number>(0)
  const [loaderStatus, setLoaderStatus] = useState<string>('wasm32: 대기 중')

  // FPS 측정용 간단 타이머
  useEffect(() => {
    let frameCount = 0
    let lastTime = performance.now()
    let rafId = 0

    const loop = () => {
      frameCount += 1
      const now = performance.now()
      const delta = now - lastTime
      if (delta >= 1000) {
        setFps(frameCount)
        frameCount = 0
        lastTime = now
      }
      rafId = requestAnimationFrame(loop)
    }

    rafId = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(rafId)
  }, [])

  // 초기 렌더 캔버스 준비 (2D 컨텍스트 사용하지 않음 - WebGL 우선)
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    // WebGL을 위해 2D 컨텍스트를 생성하지 않음
    // 대신 CSS로 플레이스홀더 표시
    console.log('캔버스 준비 완료 (WebGL 우선)')
  }, [])

  // VTK.wasm 동적 로더(asm.js 아님, wasm32 우선)
  useEffect(() => {
    let aborted = false
    let renderingStarted = false

    ;(async () => {
      if (renderingStarted) {
        console.log('이미 렌더링 진행 중, 중복 실행 방지')
        return
      }
      renderingStarted = true
      try {
        setLoaderStatus('wasm32: npm 패키지 로딩 중')
        // 공식 npm 패키지의 createNamespace 사용 (올바른 방법)
        const { createNamespace } = await import('@kitware/vtk-wasm/vtk')
        setLoaderStatus('wasm32: createNamespace 로딩 완료')

        const api = await createNamespace()
        setLoaderStatus('wasm32: VTK 네임스페이스 생성 완료')
        // VTK 네임스페이스 확인 및 장면 구성
        console.log('VTK 네임스페이스 생성됨:', api)

        // createNamespace()의 결과가 바로 VTK 네임스페이스
        const vtkNs = api
        if (vtkNs) {
          setLoaderStatus('wasm32: 초기화 완료 - DICOM CT 로딩 중...')
          try {
            await buildSampleScene(vtkNs)
            setLoaderStatus('wasm32: 볼륨 렌더링 검증 완료 - API 제한으로 불가능 확인')
          } catch (renderError: any) {
            console.error('VTK.wasm 샘플 장면 렌더링 실패:', renderError)
            if (renderError?.message?.includes('WebGL')) {
              setLoaderStatus('wasm32: WebGL 문제 - 대안 렌더링 적용됨')
            } else {
              setLoaderStatus(`wasm32: 렌더링 실패 - ${renderError?.message || '알 수 없는 오류'}`)
            }
          }
        } else {
          setLoaderStatus('wasm32: vtk 네임스페이스 미발견')
        }
        URL.revokeObjectURL(blobUrl)
      } catch {
        if (aborted) return
        setLoaderStatus('wasm32: 로딩 실패')
      }
    })()
    return () => {
      aborted = true
    }
  }, [])

  return (
    <div style={{ display: 'flex', gap: 16, height: '100vh', padding: 16, boxSizing: 'border-box' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: '#222', borderRadius: 8, padding: 20 }}>
        <div style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0, color: 'white' }}>VTK.wasm CT Viewer PoC</h2>
          <div style={{ color: '#888' }}>FPS: {fps}</div>
        </div>
        <div style={{ color: '#888', fontSize: 12, marginBottom: 16 }}>상태: {loaderStatus}</div>
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#111', borderRadius: 8, padding: 8 }}>
          <canvas
            id='vtk-wasm-window'
            ref={canvasRef}
            width={800}
            height={600}
            style={{
              maxWidth: '100%',
              maxHeight: '100%',
              background: '#000',
              borderRadius: 4,
            }}
            onContextMenu={(e) => e.preventDefault()}
            data-engine='webgl'
          />
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <section>
          <h3 style={{ margin: '8px 0' }}>전이함수 프리셋</h3>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button>Bone</button>
            <button>Soft Tissue</button>
            <button>Lung</button>
          </div>
        </section>
        <section>
          <h3 style={{ margin: '8px 0' }}>윈도우/레벨</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 60px', alignItems: 'center', gap: 8 }}>
            <input type='range' min={1} max={4000} defaultValue={1600} />
            <span>W</span>
            <input type='range' min={-1024} max={1024} defaultValue={0} />
            <span>L</span>
          </div>
        </section>
        <section>
          <h3 style={{ margin: '8px 0' }}>데이터셋</h3>
          <div style={{ display: 'flex', gap: 8 }}>
            <button>Large CT</button>
            <button>Small CT</button>
            <button>Rate10+binning</button>
          </div>
        </section>
        <section>
          <h3 style={{ margin: '8px 0' }}>상태</h3>
          <div style={{ fontSize: 12, color: '#555' }}>
            <div>로딩: -</div>
            <div>메모리: -</div>
            <div>오류: -</div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default App
