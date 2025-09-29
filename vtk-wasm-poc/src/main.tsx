/*
 * VTK.wasm POC - 엔트리 및 샘플 장면 구성자
 *
 * Copyright (c) Ewoosoft Co., Ltd.
 *
 * All rights reserved.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

/**
 * 클라이언트 사이드 VTK.wasm 장면 구성 함수
 * 공식 문서 예제 코드 기반으로 구현
 */
async function buildClientSideVTKScene(vtk: any) {
  console.log('클라이언트 사이드 VTK.wasm 장면 구성 시작')

  try {
    // 공식 문서의 makeQuadMesh 함수
    function makeQuadMesh(nx: number, ny: number) {
      const pointJSArray = []
      for (let i = 0; i < ny + 1; i++) {
        for (let j = 0; j < nx + 1; j++) {
          const x = (j - 0.5 * nx) / nx
          const y = (i - 0.5 * ny) / ny
          pointJSArray.push(x) // x-coordinate
          pointJSArray.push(y) // y-coordinate
          pointJSArray.push(2 * Math.sqrt(x * x + y * y) * Math.sin(x) * Math.cos(y)) // z-coordinate
        }
      }

      const connectivityJSArray = []
      const offsetsJSArray = []
      for (let i = 0; i < ny; i++) {
        for (let j = 0; j < nx; j++) {
          offsetsJSArray.push(connectivityJSArray.length)
          connectivityJSArray.push(j + i * (nx + 1))
          connectivityJSArray.push(j + i * (nx + 1) + 1)
          connectivityJSArray.push(j + i * (nx + 1) + nx + 2)
          connectivityJSArray.push(j + i * (nx + 1) + nx + 1)
        }
      }
      offsetsJSArray.push(connectivityJSArray.length)

      return {
        points: pointJSArray,
        offsets: offsetsJSArray,
        connectivity: connectivityJSArray,
      }
    }

    const meshData = makeQuadMesh(20, 20)

    // VTK 객체 생성 (공식 문서 예제)
    console.log('VTK 객체들 생성 중...')
    const points = vtk.vtkPoints()
    const polys = vtk.vtkCellArray()
    const connectivity = vtk.vtkTypeInt32Array()
    const offsets = vtk.vtkTypeInt32Array()

    // JavaScript 데이터를 VTK.wasm 타입으로 바인딩
    console.log('데이터 바인딩 중...')
    await points.data.setArray(new Float32Array(meshData.points))
    await connectivity.setArray(new Int32Array(meshData.connectivity))
    await offsets.setArray(new Int32Array(meshData.offsets))

    // 셀 배열 설정
    await polys.setData(offsets, connectivity)

    // PolyData 생성
    const polyData = vtk.vtkPolyData()
    polyData.set({ points, polys })

    console.log('NumberOfPoints:', await polyData.getNumberOfPoints())
    console.log('NumberOfCells:', await polyData.getNumberOfCells())

    // 매퍼와 액터 생성
    const mapper = vtk.vtkPolyDataMapper()
    await mapper.setInputData(polyData)
    const actor = vtk.vtkActor({ mapper })

    // 엣지 표시 활성화
    actor.property.edgeVisibility = true

    // 렌더러 설정
    const renderer = vtk.vtkRenderer()
    await renderer.addActor(actor)
    await renderer.resetCamera()

    // 캔버스 확인 및 WebGL 컨텍스트 테스트
    const canvas = document.getElementById('vtk-wasm-window') as HTMLCanvasElement
    if (!canvas) {
      throw new Error('캔버스를 찾을 수 없습니다')
    }

    // WebGL 컨텍스트 사전 테스트
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl')
    if (!gl) {
      throw new Error('WebGL 컨텍스트를 생성할 수 없습니다. 브라우저에서 WebGL을 지원하지 않습니다.')
    }
    console.log('WebGL 컨텍스트 사전 테스트 성공:', gl.getParameter(gl.VERSION))

    // 렌더 윈도우 생성 및 캔버스 바인딩
    const canvasSelector = '#vtk-wasm-window'
    console.log('렌더 윈도우 생성 중...')
    const renderWindow = vtk.vtkRenderWindow({ canvasSelector })
    await renderWindow.addRenderer(renderer)

    console.log('인터랙터 생성 중...')
    const interactor = vtk.vtkRenderWindowInteractor({
      canvasSelector,
      renderWindow,
    })

    // 렌더링 시작
    console.log('렌더링 시작...')
    await interactor.render()
    await interactor.start()

    console.log('클라이언트 사이드 VTK.wasm 3D 장면 렌더링 완료!')
    return true
  } catch (error) {
    console.error('클라이언트 사이드 VTK.wasm 장면 구성 실패:', error)
    throw error
  }
}

/**
 * ClassHandle 기반 VTK 장면 구성 함수
 * trame 스타일의 원격 호출을 통한 VTK 렌더링
 */
async function buildVTKSceneWithClassHandle(session: any) {
  console.log('ClassHandle 기반 VTK 장면 구성 시작')

  try {
    // 렌더러 생성
    console.log('렌더러 생성...')
    const renderer = await session.invoke('vtkRenderer')
    console.log('렌더러 생성 결과:', renderer)

    // 렌더 윈도우 생성
    console.log('렌더 윈도우 생성...')
    const renderWindow = await session.invoke('vtkRenderWindow')
    console.log('렌더 윈도우 생성 결과:', renderWindow)

    // 렌더 윈도우에 렌더러 추가
    if (renderWindow && renderer) {
      await renderWindow.invoke('AddRenderer', renderer)
      console.log('렌더러를 렌더 윈도우에 추가 완료')
    }

    // 인터랙터 생성 및 캔버스 연결
    console.log('인터랙터 생성...')
    const interactor = await session.invoke('vtkRenderWindowInteractor')
    if (interactor && renderWindow) {
      await interactor.invoke('SetRenderWindow', renderWindow)
      console.log('인터랙터에 렌더 윈도우 설정 완료')

      // 캔버스 연결 시도
      const canvas = document.getElementById('vtk-wasm-window') as HTMLCanvasElement
      if (canvas) {
        // ClassHandle 기반에서는 다른 방식으로 캔버스를 연결해야 할 수 있음
        console.log('캔버스 연결 시도:', canvas)
        await interactor.invoke('Initialize')
        await interactor.invoke('Start')
        console.log('인터랙터 초기화 및 시작 완료')
      }
    }

    console.log('ClassHandle 기반 VTK 장면 구성 완료')
    return true
  } catch (error) {
    console.error('ClassHandle 기반 VTK 장면 구성 실패:', error)
    throw error
  }
}

/**
 * VTK.wasm 샘플 장면 구성 함수
 * VTK.wasm JavaScript 가이드의 예제 코드를 기반으로 구현
 */
export async function buildSampleScene(vtk: any) {
  console.log('VTK.wasm 네임스페이스:', vtk)
  console.log('VTK 객체 키들:', Object.keys(vtk))
  console.log('vtkPoints 존재 여부:', typeof vtk.vtkPoints)

  // 클라이언트 사이드 VTK.wasm 직접 사용 시도
  if (typeof vtk.vtkPoints === 'function') {
    console.log('클라이언트 사이드 VTK 팩토리 함수 발견! 직접 렌더링 시도')
    return await buildClientSideVTKScene(vtk)
  }

  console.log('VTK 팩토리 함수를 찾을 수 없음. 다른 접근 시도...')

  // VTK.wasm 세션 기반 접근 시도 (이전 코드)
  if (typeof vtk.vtkPoints !== 'function') {
    console.log('직접 vtk.vtkPoints를 찾을 수 없음. 세션 기반 접근 시도...')

    // vtkStandaloneSession을 통한 접근 시도
    if (typeof vtk.vtkStandaloneSession === 'function') {
      console.log('vtkStandaloneSession을 통한 VTK 객체 접근 시도')
      try {
        const session = new vtk.vtkStandaloneSession()
        console.log('세션 생성 완료:', session)
        console.log('세션 객체 키들:', Object.keys(session))
        console.log('세션 타입:', typeof session)

        // ClassHandle의 프로토타입 메서드들 확인
        console.log('세션 프로토타입:', Object.getPrototypeOf(session))
        console.log('세션 프로토타입 키들:', Object.getOwnPropertyNames(Object.getPrototypeOf(session)))

        // 세션 초기화 시도
        console.log('세션 초기화 시도...')
        if (typeof session.initialize === 'function') {
          console.log('initialize 메서드 발견, 호출 중...')
          await session.initialize()
          console.log('세션 초기화 완료')
        } else {
          console.log('initialize 메서드 없음, 바로 진행')
        }

        // ClassHandle의 invoke 메서드를 통한 VTK 객체 접근 시도
        console.log('ClassHandle invoke 메서드를 통한 VTK 객체 생성 시도')

        // invoke 메서드 존재 여부 확인
        if (typeof session.invoke === 'function') {
          console.log('invoke 메서드 발견')

          // VTK.wasm에서는 invoke가 다른 용도일 수 있음. 다른 접근 시도
          try {
            // 세션에서 직접 VTK 팩토리 함수들 찾기
            console.log('세션에서 VTK 팩토리 함수 탐색...')

            // 가능한 VTK 네임스페이스 위치들 확인
            const possibleVtkLocations = [session.vtk, session.getVTK && session.getVTK(), session.api, session.objects, session]

            for (const vtkCandidate of possibleVtkLocations) {
              if (vtkCandidate && typeof vtkCandidate.vtkPoints === 'function') {
                console.log('VTK 팩토리 함수들 발견!', vtkCandidate)
                return buildSampleScene(vtkCandidate)
              }
            }

            // 세션의 모든 메서드 시도
            console.log('세션의 모든 메서드 탐색...')
            const sessionMethods = Object.getOwnPropertyNames(Object.getPrototypeOf(session))
            for (const methodName of sessionMethods) {
              if (typeof (session as any)[methodName] === 'function' && methodName !== 'constructor') {
                try {
                  console.log(`${methodName} 메서드 호출 시도...`)
                  const result = await (session as any)[methodName]()
                  if (result && typeof result.vtkPoints === 'function') {
                    console.log(`${methodName}()에서 VTK 팩토리 발견!`)
                    return buildSampleScene(result)
                  }
                } catch (e) {
                  console.log(`${methodName}() 호출 실패:`, e.message)
                }
              }
            }
          } catch (sessionError) {
            console.log('세션 탐색 실패:', sessionError)
          }
        } else {
          console.log('invoke 메서드 없음')
        }

        // 세션의 다른 메서드들 확인
        console.log('세션 프로퍼티들:', Object.getOwnPropertyNames(session))
      } catch (sessionError) {
        console.error('세션 생성 실패:', sessionError)
      }
    }

    throw new Error('VTK 팩토리 함수들을 찾을 수 없습니다. 세션 기반 접근도 실패했습니다.')
  }

  try {
    // 간단한 쿼드 메시 생성 (JavaScript로 데이터 생성)
    function makeQuadMesh(nx: number, ny: number) {
      const pointJSArray = []
      for (let i = 0; i < ny + 1; i++) {
        for (let j = 0; j < nx + 1; j++) {
          const x = (j - 0.5 * nx) / nx
          const y = (i - 0.5 * ny) / ny
          pointJSArray.push(x) // x-coordinate
          pointJSArray.push(y) // y-coordinate
          pointJSArray.push(2 * Math.sqrt(x * x + y * y) * Math.sin(x) * Math.cos(y)) // z-coordinate
        }
      }

      const connectivityJSArray = []
      const offsetsJSArray = []
      for (let i = 0; i < ny; i++) {
        for (let j = 0; j < nx; j++) {
          offsetsJSArray.push(connectivityJSArray.length)
          connectivityJSArray.push(j + i * (nx + 1))
          connectivityJSArray.push(j + i * (nx + 1) + 1)
          connectivityJSArray.push(j + i * (nx + 1) + nx + 2)
          connectivityJSArray.push(j + i * (nx + 1) + nx + 1)
        }
      }
      offsetsJSArray.push(connectivityJSArray.length)

      return {
        points: pointJSArray,
        offsets: offsetsJSArray,
        connectivity: connectivityJSArray,
      }
    }

    const meshData = makeQuadMesh(20, 20)

    // VTK.wasm 객체 생성
    const points = vtk.vtkPoints()
    const polys = vtk.vtkCellArray()
    const connectivity = vtk.vtkTypeInt32Array()
    const offsets = vtk.vtkTypeInt32Array()

    // JavaScript 데이터를 VTK.wasm 타입으로 바인딩
    await points.data.setArray(new Float32Array(meshData.points))
    await connectivity.setArray(new Int32Array(meshData.connectivity))
    await offsets.setArray(new Int32Array(meshData.offsets))

    // 셀 배열 설정
    await polys.setData(offsets, connectivity)

    // PolyData 생성
    const polyData = vtk.vtkPolyData()
    polyData.set({ points, polys })

    console.log('NumberOfPoints:', await polyData.getNumberOfPoints())
    console.log('NumberOfCells:', await polyData.getNumberOfCells())

    // 매퍼와 액터 생성
    const mapper = vtk.vtkPolyDataMapper()
    await mapper.setInputData(polyData)
    const actor = vtk.vtkActor({ mapper })

    // 엣지 표시 활성화
    actor.property.edgeVisibility = true

    // 렌더러 설정
    const renderer = vtk.vtkRenderer()
    await renderer.addActor(actor)
    await renderer.resetCamera()

    // 렌더 윈도우 생성 및 캔버스 바인딩
    const canvasSelector = '#vtk-wasm-window'
    const renderWindow = vtk.vtkRenderWindow({ canvasSelector })
    await renderWindow.addRenderer(renderer)
    const interactor = vtk.vtkRenderWindowInteractor({
      canvasSelector,
      renderWindow,
    })

    // 렌더링 시작
    await interactor.render()
    await interactor.start()

    console.log('VTK.wasm 3D 장면 렌더링 완료')
  } catch (error) {
    console.error('VTK.wasm 장면 구성 실패:', error)

    // 폴백: 캔버스에 오류 메시지 표시
    const canvas = document.getElementById('vtk-wasm-window') as HTMLCanvasElement
    if (canvas) {
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.fillStyle = '#222'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.fillStyle = '#f44'
        ctx.font = '16px sans-serif'
        ctx.fillText('VTK.wasm 렌더링 실패', 20, 50)
        ctx.fillStyle = '#fff'
        ctx.font = '12px sans-serif'
        ctx.fillText(`오류: ${error}`, 20, 80)
      }
    }
    throw error
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
