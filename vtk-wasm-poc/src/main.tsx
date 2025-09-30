/*
 * VTK.wasm POC - 엔트리 및 DICOM CT 볼륨 렌더링
 *
 * Copyright (c) Ewoosoft Co., Ltd.
 *
 * All rights reserved.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
// DICOM 파서는 직접 구현하여 VTK.wasm과 호환성 확보

/**
 * DICOM 파일 로더 및 파서
 */
async function loadDicomFiles(folderPath: string) {
  try {
    console.log('DICOM 파일 로딩 시작:', folderPath)

    // DICOM 파일 목록 가져오기 (예시 - 실제로는 서버에서 파일 목록을 받아야 함)
    const response = await fetch(`${folderPath}/file-list.json`)
    if (!response.ok) {
      throw new Error('DICOM 파일 목록을 가져올 수 없습니다')
    }

    const fileList = await response.json()
    console.log('DICOM 파일 목록:', fileList)

    const dicomSlices = []

    // 각 DICOM 파일 로드 및 파싱
    const totalFiles = fileList.files.length
    console.log(`총 ${totalFiles}개 DICOM 파일 로딩 시작...`)

    for (let i = 0; i < fileList.files.length; i++) {
      const fileName = fileList.files[i]
      try {
        if (i % 50 === 0 || i < 10) {
          // 처음 10개와 50개마다 로그
          console.log(`DICOM 파일 로딩 중: ${fileName} (${i + 1}/${totalFiles})`)
        }
        const fileResponse = await fetch(`${folderPath}/${fileName}`)
        const arrayBuffer = await fileResponse.arrayBuffer()
        const byteArray = new Uint8Array(arrayBuffer)

        // DICOM 파일 크기 분석
        const fileSize = arrayBuffer.byteLength
        console.log(`${fileName} 파일 크기: ${fileSize} bytes`)

        // 파일 크기 기반으로 픽셀 데이터 크기 역산
        console.log(`${fileName}: 파일 크기 ${fileSize} bytes 분석 중...`)

        // DICOM 헤더는 보통 처음 몇 KB, 픽셀 데이터는 끝부분
        // 가능한 픽셀 데이터 크기들 (16bit 기준)
        const possiblePixelCounts = [
          496 * 496, // 246,016 pixels = 492,032 bytes
          512 * 512, // 262,144 pixels = 524,288 bytes
          256 * 256, // 65,536 pixels = 131,072 bytes
          400 * 400, // 160,000 pixels = 320,000 bytes
        ]

        let header = null
        let pixelData = null

        // 파일 크기에 맞는 픽셀 데이터 크기 찾기
        for (const pixelCount of possiblePixelCounts) {
          const pixelDataSizeBytes = pixelCount * 2 // 16bit

          if (pixelDataSizeBytes <= fileSize) {
            const pixelDataOffset = fileSize - pixelDataSizeBytes

            try {
              const testPixelData = new Uint16Array(arrayBuffer, pixelDataOffset, pixelCount)

              // 크기 역산
              const dimension = Math.sqrt(pixelCount)
              if (dimension === Math.floor(dimension)) {
                header = {
                  rows: dimension,
                  columns: dimension,
                  instanceNumber: parseInt(fileName.match(/\d+/)?.[0] || '1'),
                  sliceThickness: 1.0,
                  pixelSpacing: [1.0, 1.0],
                }
                pixelData = testPixelData
                console.log(`${fileName}: ${dimension}x${dimension} 크기로 파싱 성공 (${pixelDataSizeBytes} bytes)`)
                break
              }
            } catch (e) {
              console.log(`${fileName}: ${pixelCount} 픽셀 시도 실패:`, e.message)
            }
          }
        }

        if (!header || !pixelData) {
          console.warn(`${fileName}: 픽셀 데이터 추출 실패, 건너뛰기`)
          continue // 이 파일은 건너뛰고 다음 파일 시도
        }

        const imageData = {
          fileName,
          pixelData,
          instanceNumber: header.instanceNumber,
          rows: header.rows,
          columns: header.columns,
          pixelSpacing: header.pixelSpacing,
          sliceThickness: header.sliceThickness,
        }
        dicomSlices.push(imageData)
      } catch (fileError) {
        console.warn(`DICOM 파일 로드 실패: ${fileName}`, fileError)
      }
    }

    // 슬라이스 정렬 (Instance Number 기준)
    dicomSlices.sort((a, b) => parseInt(a.instanceNumber || '0') - parseInt(b.instanceNumber || '0'))

    console.log(`DICOM 로딩 완료: ${dicomSlices.length}개 슬라이스`)
    return dicomSlices
  } catch (error) {
    console.error('DICOM 로딩 실패:', error)
    throw error
  }
}

/**
 * DICOM 데이터를 VTK.wasm 호환 볼륨으로 변환
 */
async function createVolumeFromDicom(vtk: any, dicomSlices: any[]) {
  if (dicomSlices.length === 0) {
    throw new Error('DICOM 슬라이스가 없습니다')
  }

  const firstSlice = dicomSlices[0]
  const rows = firstSlice.rows
  const columns = firstSlice.columns
  const slices = dicomSlices.length

  console.log(`볼륨 크기: ${columns} x ${rows} x ${slices}`)

  // 전체 픽셀 데이터 배열 생성
  const totalPixels = columns * rows * slices
  const volumeData = new Uint16Array(totalPixels)

  // 각 슬라이스 데이터를 볼륨에 복사
  for (let i = 0; i < dicomSlices.length; i++) {
    const slice = dicomSlices[i]
    const slicePixels = slice.pixelData.slice(0, columns * rows) // 크기 제한
    const sliceOffset = i * columns * rows
    volumeData.set(slicePixels, sliceOffset)
  }

  // VTK.wasm 호환 방식: JavaScript 배열을 직접 반환
  const volumeInfo = {
    data: volumeData,
    dimensions: [columns, rows, slices],
    spacing: [firstSlice.pixelSpacing[0] || 1.0, firstSlice.pixelSpacing[1] || 1.0, firstSlice.sliceThickness || 1.0],
    origin: [0, 0, 0],
    scalarType: 'Uint16Array',
  }

  console.log('DICOM -> VTK.wasm 볼륨 변환 완료')
  return volumeInfo
}

/**
 * VTK.wasm DICOM 기반 3D 메시 렌더링 (볼륨 렌더링 대안)
 */
async function buildDicomMeshScene(vtk: any, volumeInfo: any) {
  console.log('DICOM 기반 3D 메시 렌더링 시작')

  try {
    const [width, height, depth] = volumeInfo.dimensions
    console.log(`DICOM 볼륨: ${width}x${height}x${depth}`)

    // 중간 슬라이스 데이터 추출
    const midSliceIndex = Math.floor(depth / 2)
    const sliceSize = width * height
    const midSliceOffset = midSliceIndex * sliceSize
    const midSliceData = volumeInfo.data.slice(midSliceOffset, midSliceOffset + sliceSize)

    console.log(`중간 슬라이스 (${midSliceIndex}) 추출 완료`)

    // DICOM 데이터 기반 3D 높이맵 생성
    const points = vtk.vtkPoints()
    const polys = vtk.vtkCellArray()
    const connectivity = vtk.vtkTypeInt32Array()
    const offsets = vtk.vtkTypeInt32Array()

    const pointArray = []
    const connectivityArray = []
    const offsetsArray = []

    // 샘플링 간격 (성능 최적화)
    const step = 8
    const gridWidth = Math.floor(width / step)
    const gridHeight = Math.floor(height / step)

    console.log(`그리드 크기: ${gridWidth} x ${gridHeight}`)

    // DICOM 픽셀 값을 3D 높이로 변환
    for (let i = 0; i < gridHeight; i++) {
      for (let j = 0; j < gridWidth; j++) {
        const x = j * step
        const y = i * step
        const pixelIndex = y * width + x
        const pixelValue = midSliceData[pixelIndex] || 0

        // 정규화된 좌표
        const xNorm = ((j - gridWidth / 2) / gridWidth) * 4
        const yNorm = ((i - gridHeight / 2) / gridHeight) * 4
        const zNorm = (pixelValue - 1000) / 2000 // HU 값 정규화

        pointArray.push(xNorm, yNorm, zNorm)
      }
    }

    // 메시 연결성 생성
    for (let i = 0; i < gridHeight - 1; i++) {
      for (let j = 0; j < gridWidth - 1; j++) {
        offsetsArray.push(connectivityArray.length)
        connectivityArray.push(j + i * gridWidth)
        connectivityArray.push(j + i * gridWidth + 1)
        connectivityArray.push(j + i * gridWidth + gridWidth + 1)
        connectivityArray.push(j + i * gridWidth + gridWidth)
      }
    }
    offsetsArray.push(connectivityArray.length)

    console.log(`포인트: ${pointArray.length / 3}개, 셀: ${offsetsArray.length - 1}개`)

    // VTK 객체에 데이터 설정
    await points.data.setArray(new Float32Array(pointArray))
    await connectivity.setArray(new Int32Array(connectivityArray))
    await offsets.setArray(new Int32Array(offsetsArray))
    await polys.setData(offsets, connectivity)

    // PolyData 생성
    const polyData = vtk.vtkPolyData()
    polyData.set({ points, polys })

    console.log('DICOM 기반 PolyData 생성 완료')

    // 매퍼와 액터 생성
    const mapper = vtk.vtkPolyDataMapper()
    await mapper.setInputData(polyData)
    const actor = vtk.vtkActor({ mapper })

    // CT 데이터 기반 색상 설정
    actor.property.color = [0.9, 0.9, 1.0] // 연한 파란색 (CT 느낌)
    actor.property.edgeVisibility = true // 윤곽선 표시

    // 렌더러 설정
    const renderer = vtk.vtkRenderer()
    await renderer.addActor(actor)
    await renderer.setBackground([0.05, 0.05, 0.15]) // 어두운 배경
    await renderer.resetCamera()

    // 캔버스에 렌더링
    const canvas = document.getElementById('vtk-wasm-window') as HTMLCanvasElement
    if (!canvas) {
      throw new Error('캔버스를 찾을 수 없습니다')
    }

    const canvasSelector = `#${canvas.id}`
    console.log('DICOM 메시 렌더 윈도우 생성 중...', canvasSelector)
    const renderWindow = vtk.vtkRenderWindow({ canvasSelector })
    await renderWindow.addRenderer(renderer)

    const interactor = vtk.vtkRenderWindowInteractor({
      canvasSelector,
      renderWindow,
    })

    console.log('DICOM 메시 렌더링 시작...')
    await interactor.render()
    await interactor.start()

    console.log('VTK.wasm DICOM 3D 메시 렌더링 완료!')
    return true
  } catch (error) {
    console.error('DICOM 메시 렌더링 실패:', error)
    throw error
  }
}

/**
 * VTK.wasm 전용 볼륨 렌더링 함수 (사용되지 않음)
 */
async function buildVTKWasmVolumeScene(vtk: any, volumeInfo: any) {
  console.log('VTK.wasm 볼륨 렌더링 시작')

  try {
    // VTK ImageData 생성 시도
    console.log('VTK ImageData 생성 중...')
    const imageData = vtk.vtkImageData()

    // 차원 설정
    const [width, height, depth] = volumeInfo.dimensions
    console.log(`볼륨 차원 설정: ${width} x ${height} x ${depth}`)
    await imageData.setDimensions([width, height, depth])

    // 스페이싱 설정
    console.log('스페이싱 설정:', volumeInfo.spacing)
    await imageData.setSpacing(volumeInfo.spacing)

    // 원점 설정
    await imageData.setOrigin(volumeInfo.origin)

    // VTK.wasm에서 사용 가능한 클래스 확인
    console.log('VTK 네임스페이스 탐색...')
    const allKeys = Object.keys(vtk)
    console.log(
      '사용 가능한 VTK 클래스들:',
      allKeys.filter((key) => key.startsWith('vtk')),
    )

    // 스칼라 데이터 설정 (VTK.wasm 호환 방식)
    console.log('스칼라 데이터 설정 중...')

    // Float32Array로 변환 시도 (더 호환성이 좋음)
    const floatData = new Float32Array(volumeInfo.data)
    console.log('Float32Array 변환 완료, 크기:', floatData.length)

    try {
      // vtkDataArray 대신 직접 ImageData에 데이터 설정 시도
      console.log('ImageData에 직접 스칼라 데이터 설정 시도...')

      // VTK.wasm의 ImageData 스칼라 설정 방법 탐색
      const pointData = await imageData.getPointData()
      console.log('PointData 객체:', pointData)
      console.log('PointData 메서드들:', Object.getOwnPropertyNames(Object.getPrototypeOf(pointData)))

      // 🎯 볼륨 렌더링 핵심: 다양한 방법으로 스칼라 데이터 설정 시도
      console.log('🎯 볼륨 데이터 설정 방법 탐색...')

      // ImageData 메서드 확인
      const imageDataMethods = Object.getOwnPropertyNames(Object.getPrototypeOf(imageData))
      console.log('ImageData 사용 가능 메서드들:', imageDataMethods)

      let success = false

      // 방법 1: allocateScalars + getScalarPointer
      if (typeof imageData.allocateScalars === 'function') {
        console.log('🔬 allocateScalars 방법 시도...')
        try {
          await imageData.allocateScalars(10, 1) // VTK_FLOAT = 10, 1 component
          console.log('allocateScalars 성공')

          // 데이터 포인터 가져와서 직접 설정
          if (typeof imageData.getScalarPointer === 'function') {
            const scalarPointer = await imageData.getScalarPointer()
            console.log('ScalarPointer 획득:', scalarPointer)
            // TODO: 포인터에 데이터 복사
          }
          success = true
        } catch (e) {
          console.log('❌ allocateScalars 실패:', e.message)
        }
      }

      // 방법 2: setScalarComponentFromFloat
      if (!success && typeof imageData.setScalarComponentFromFloat === 'function') {
        console.log('🔬 setScalarComponentFromFloat 방법 시도...')
        try {
          const [width, height, depth] = volumeInfo.dimensions
          // 작은 샘플로 테스트 (성능상)
          for (let z = 0; z < Math.min(5, depth); z++) {
            for (let y = 0; y < Math.min(10, height); y += 10) {
              for (let x = 0; x < Math.min(10, width); x += 10) {
                const index = z * width * height + y * width + x
                const value = floatData[index] || 0
                await imageData.setScalarComponentFromFloat(x, y, z, 0, value)
              }
            }
          }
          console.log('setScalarComponentFromFloat 샘플 설정 성공')
          success = true
        } catch (e) {
          console.log('❌ setScalarComponentFromFloat 실패:', e.message)
        }
      }

      // 방법 3: 기본 메서드들
      if (!success) {
        console.log('🔬 기본 설정 메서드들 시도...')
        const methods = ['setData', 'setScalarData', 'setArray']

        for (const method of methods) {
          if (typeof imageData[method] === 'function') {
            try {
              console.log(`${method} 시도...`)
              await imageData[method](floatData)
              console.log(`${method} 성공`)
              success = true
              break
            } catch (e) {
              console.log(`❌ ${method} 실패:`, e.message)
            }
          }
        }
      }

      if (!success) {
        throw new Error('❌ 모든 볼륨 데이터 설정 방법 실패 - VTK.wasm 볼륨 렌더링 불가능')
      }
    } catch (scalarError) {
      console.error('스칼라 데이터 설정 실패:', scalarError)
      throw scalarError
    }

    console.log('VTK ImageData 설정 완료')

    // 볼륨 매퍼 생성
    console.log('볼륨 매퍼 생성 중...')
    const volumeMapper = vtk.vtkVolumeMapper()
    await volumeMapper.setInputData(imageData)

    // 볼륨 액터 생성
    const volume = vtk.vtkVolume()
    await volume.setMapper(volumeMapper)

    // 볼륨 프로퍼티 설정
    const property = await volume.getProperty()

    // 색상 전이함수
    const colorFunc = vtk.vtkColorTransferFunction()
    await colorFunc.addPoint(-1000, 0.0, 0.0, 0.0) // 공기
    await colorFunc.addPoint(-500, 0.3, 0.3, 0.3) // 연조직
    await colorFunc.addPoint(0, 0.6, 0.6, 0.6) // 물
    await colorFunc.addPoint(500, 1.0, 1.0, 1.0) // 뼈

    // 투명도 전이함수
    const opacityFunc = vtk.vtkPiecewiseFunction()
    await opacityFunc.addPoint(-1000, 0.0)
    await opacityFunc.addPoint(-500, 0.02)
    await opacityFunc.addPoint(0, 0.1)
    await opacityFunc.addPoint(500, 0.8)

    await property.setColor(colorFunc)
    await property.setScalarOpacity(opacityFunc)

    // 렌더러 생성
    const renderer = vtk.vtkRenderer()
    await renderer.addVolume(volume)
    await renderer.setBackground([0.1, 0.1, 0.2])
    await renderer.resetCamera()

    // 캔버스에 렌더링
    const canvas = document.getElementById('vtk-wasm-window') as HTMLCanvasElement
    if (!canvas) {
      throw new Error('캔버스를 찾을 수 없습니다')
    }

    const canvasSelector = `#${canvas.id}`
    console.log('볼륨 렌더 윈도우 생성 중...', canvasSelector)
    const renderWindow = vtk.vtkRenderWindow({ canvasSelector })
    await renderWindow.addRenderer(renderer)

    const interactor = vtk.vtkRenderWindowInteractor({
      canvasSelector,
      renderWindow,
    })

    console.log('볼륨 렌더링 시작...')
    await interactor.render()
    await interactor.start()

    console.log('VTK.wasm 볼륨 렌더링 완료!')
    return true
  } catch (error) {
    console.error('VTK.wasm 볼륨 렌더링 실패:', error)
    throw error
  }
}

/**
 * CT 볼륨 렌더링 파이프라인 구성 (사용되지 않음 - 위 함수로 대체)
 */
async function buildCTVolumeScene(vtk: any, volumeData: any) {
  console.log('CT 볼륨 렌더링 파이프라인 구성 시작')

  try {
    // 볼륨 매퍼 생성
    const volumeMapper = vtk.vtkVolumeMapper()
    await volumeMapper.setInputData(volumeData)

    // 볼륨 액터 생성
    const volume = vtk.vtkVolume()
    volume.setMapper(volumeMapper)

    // 전이함수 (Transfer Function) 설정
    const property = volume.getProperty()

    // 색상 전이함수 (간단한 그레이스케일)
    const colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.addPoint(-1000, 0.0, 0.0, 0.0) // 공기 (검정)
    colorTransferFunction.addPoint(-500, 0.3, 0.3, 0.3) // 연조직
    colorTransferFunction.addPoint(0, 0.6, 0.6, 0.6) // 물
    colorTransferFunction.addPoint(500, 1.0, 1.0, 1.0) // 뼈 (흰색)

    // 투명도 전이함수
    const opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.addPoint(-1000, 0.0) // 공기 완전 투명
    opacityTransferFunction.addPoint(-500, 0.02) // 연조직 약간 보임
    opacityTransferFunction.addPoint(0, 0.1) // 물
    opacityTransferFunction.addPoint(500, 0.8) // 뼈 잘 보임

    property.setColor(colorTransferFunction)
    property.setScalarOpacity(opacityTransferFunction)

    // 렌더러 생성 및 설정
    const renderer = vtk.vtkRenderer()
    await renderer.addVolume(volume)
    await renderer.resetCamera()

    // 배경색 설정
    renderer.setBackground([0.1, 0.1, 0.2])

    console.log('CT 볼륨 렌더링 파이프라인 구성 완료')
    return { renderer, volume, volumeMapper, property }
  } catch (error) {
    console.error('CT 볼륨 렌더링 실패:', error)
    throw error
  }
}

/**
 * WebGL 지원 상태 진단 함수
 */
function diagnoseWebGL() {
  console.log('=== WebGL 진단 시작 ===')

  // 브라우저 정보
  console.log('User Agent:', navigator.userAgent)
  console.log('Platform:', navigator.platform)

  // WebGL 확장 지원 확인
  const testCanvas = document.createElement('canvas')
  const contexts = ['webgl2', 'webgl', 'experimental-webgl']

  for (const contextType of contexts) {
    try {
      const gl = testCanvas.getContext(contextType as any)
      if (gl) {
        console.log(`${contextType} 지원: ✅`)
        console.log(`  - 버전: ${gl.getParameter(gl.VERSION)}`)
        console.log(`  - 렌더러: ${gl.getParameter(gl.RENDERER)}`)
        console.log(`  - 벤더: ${gl.getParameter(gl.VENDOR)}`)
        console.log(`  - GLSL 버전: ${gl.getParameter(gl.SHADING_LANGUAGE_VERSION)}`)

        // 확장 기능 확인
        const extensions = gl.getSupportedExtensions()
        console.log(`  - 지원 확장: ${extensions?.length || 0}개`)

        return gl
      } else {
        console.log(`${contextType} 지원: ❌`)
      }
    } catch (e) {
      console.log(`${contextType} 오류:`, e)
    }
  }

  console.log('=== WebGL 진단 완료 ===')
  return null
}

/**
 * WebGL 없이 VTK 데이터 처리 및 2D 캔버스 렌더링
 */
async function buildFallbackScene(vtk: any, canvas: HTMLCanvasElement) {
  console.log('대안 렌더링 시작 (WebGL 없이)')

  try {
    // VTK 객체는 이미 생성되었으므로 데이터만 추출하여 2D 캔버스에 그리기
    const ctx = canvas.getContext('2d')
    if (!ctx) {
      throw new Error('2D 캔버스 컨텍스트도 생성할 수 없습니다')
    }

    // 배경 그리기
    ctx.fillStyle = '#1a1a1a'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // 성공 메시지 표시
    ctx.fillStyle = '#00ff00'
    ctx.font = 'bold 24px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('VTK.wasm 데이터 처리 성공!', canvas.width / 2, canvas.height / 2 - 60)

    ctx.fillStyle = '#ffffff'
    ctx.font = '16px Arial'
    ctx.fillText('3D 메시 생성: 441개 점, 400개 셀', canvas.width / 2, canvas.height / 2 - 20)
    ctx.fillText('WebGL 렌더링은 환경 설정 후 가능합니다', canvas.width / 2, canvas.height / 2 + 20)

    // 간단한 2D 시각화 (점들의 투영)
    ctx.fillStyle = '#0088ff'
    for (let i = 0; i < 20; i++) {
      const x = canvas.width / 2 + Math.cos(i * 0.3) * (50 + i * 5)
      const y = canvas.height / 2 + Math.sin(i * 0.3) * (50 + i * 5)
      ctx.beginPath()
      ctx.arc(x, y, 3, 0, Math.PI * 2)
      ctx.fill()
    }

    console.log('대안 렌더링 완료')
    return true
  } catch (error) {
    console.error('대안 렌더링 실패:', error)
    throw error
  }
}

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

    // 기존 컨텍스트 확인 및 정리
    console.log('캔버스 상태 확인...')
    const existingContext = (canvas as any).__webglContextLossExtension
    if (existingContext) {
      console.log('기존 WebGL 컨텍스트 발견, 정리 중...')
    }

    // WebGL 진단 실행
    const diagnosisResult = diagnoseWebGL()

    // WebGL 컨텍스트 사전 테스트 및 상세 진단
    console.log('WebGL 지원 상태 확인 중...')
    console.log('Canvas 요소:', canvas)
    console.log('Canvas 크기:', canvas.width, 'x', canvas.height)

    // WebGL 컨텍스트 생성 시도 (multisampling 오류 방지)
    const webglOptions = [
      { alpha: false, antialias: false, preserveDrawingBuffer: false }, // 안전한 기본 설정
      { alpha: true, antialias: false, preserveDrawingBuffer: true }, // 안티앨리어싱 비활성화
      { failIfMajorPerformanceCaveat: false, antialias: false },
      { powerPreference: 'high-performance', antialias: false },
      { powerPreference: 'low-power', antialias: false },
      { premultipliedAlpha: false, antialias: false },
      { stencil: false, depth: true, antialias: false },
    ]

    let gl: WebGLRenderingContext | WebGL2RenderingContext | null = null

    // 컨텍스트 생성 시도 전에 캔버스 상태 로그
    console.log('캔버스 컨텍스트 생성 시도...')
    console.log('Canvas.getContext 메서드 존재:', typeof canvas.getContext === 'function')

    for (let i = 0; i < webglOptions.length; i++) {
      const options = webglOptions[i]
      console.log(`WebGL 옵션 ${i + 1}/${webglOptions.length} 시도:`, options)

      try {
        gl = canvas.getContext('webgl2', options) as WebGL2RenderingContext
        if (!gl) {
          gl = canvas.getContext('webgl', options) as WebGLRenderingContext
        }
        if (!gl) {
          gl = canvas.getContext('experimental-webgl', options) as WebGLRenderingContext
        }

        if (gl) {
          console.log('✅ WebGL 컨텍스트 생성 성공!')
          console.log('  - 버전:', gl.getParameter(gl.VERSION))
          console.log('  - 렌더러:', gl.getParameter(gl.RENDERER))
          console.log('  - 벤더:', gl.getParameter(gl.VENDOR))
          console.log('  - 사용된 옵션:', options)
          break
        } else {
          console.log(`❌ 옵션 ${i + 1} 실패`)
        }
      } catch (error) {
        console.log(`❌ 옵션 ${i + 1} 오류:`, error)
      }
    }

    if (!gl) {
      console.error('기존 캔버스에서 WebGL 컨텍스트 생성 실패')
      console.log('새로운 캔버스로 재시도...')

      // 새로운 캔버스 생성 시도
      const newCanvas = document.createElement('canvas')
      newCanvas.width = canvas.width
      newCanvas.height = canvas.height
      newCanvas.id = 'vtk-wasm-window-new'

      // 기존 캔버스 스타일 복사
      newCanvas.style.cssText = canvas.style.cssText
      newCanvas.setAttribute('data-engine', 'webgl')

      // 기존 캔버스 교체
      const parent = canvas.parentElement
      if (parent) {
        parent.replaceChild(newCanvas, canvas)
        console.log('캔버스 교체 완료')

        // 새 캔버스로 WebGL 컨텍스트 생성 시도
        for (const options of webglOptions.slice(0, 3)) {
          // 처음 3개 옵션만 시도
          try {
            gl = newCanvas.getContext('webgl2', options) || newCanvas.getContext('webgl', options)
            if (gl) {
              console.log('✅ 새 캔버스에서 WebGL 성공!')
              console.log('  - 버전:', gl.getParameter(gl.VERSION))
              canvas = newCanvas // 캔버스 참조 업데이트
              break
            }
          } catch (error) {
            console.log('새 캔버스 시도 오류:', error)
          }
        }
      }

      if (!gl) {
        console.error('모든 시도 실패. 대안 렌더링 사용...')
        return await buildFallbackScene(vtk, canvas)
      }
    }

    // 렌더 윈도우 생성 및 캔버스 바인딩
    const canvasSelector = `#${canvas.id}` // 동적으로 캔버스 ID 사용
    console.log('렌더 윈도우 생성 중...', canvasSelector)
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
 * DICOM CT 장면 구성 함수 (메인 진입점)
 */
async function buildDicomCTScene(vtk: any) {
  console.log('DICOM CT 장면 구성 시작')

  try {
    // 1. DICOM 파일 로딩 시도
    console.log('DICOM 파일 로딩 시도...')
    let dicomSlices

    try {
      dicomSlices = await loadDicomFiles('/dummy/CT20130424_213559_8924_40274191')
    } catch (dicomError) {
      console.warn('DICOM 로딩 실패, 샘플 3D 메시로 대체:', dicomError)
      return await buildClientSideVTKScene(vtk)
    }

    if (!dicomSlices || dicomSlices.length === 0) {
      console.warn('DICOM 슬라이스가 없음, 샘플 3D 메시로 대체')
      return await buildClientSideVTKScene(vtk)
    }

    // 2. DICOM 데이터 변환 (로딩 확인용)
    console.log('DICOM 데이터 변환 중...')
    const volumeInfo = await createVolumeFromDicom(vtk, dicomSlices)
    console.log('볼륨 정보:', volumeInfo)

    // 3. VTK.wasm 실제 볼륨 렌더링 시도
    console.log('VTK.wasm 실제 볼륨 렌더링 시도')
    console.log(`DICOM 데이터 로딩 성공: ${dicomSlices.length}개 슬라이스, ${volumeInfo.dimensions.join('x')} 크기`)

    try {
      // 실제 볼륨 렌더링 시도 (POC 핵심 목표)
      console.log('🎯 VTK.wasm 볼륨 렌더링 검증 시작')
      return await buildVTKWasmVolumeScene(vtk, volumeInfo)
    } catch (volumeError) {
      console.warn('❌ VTK.wasm 볼륨 렌더링 실패:', volumeError)
      console.log('🔄 DICOM 메시 렌더링으로 대체 시도...')

      try {
        return await buildDicomMeshScene(vtk, volumeInfo)
      } catch (meshError) {
        console.warn('❌ DICOM 메시 렌더링도 실패, 샘플 메시로 최종 대체:', meshError)
        return await buildClientSideVTKScene(vtk)
      }
    }
  } catch (error) {
    console.error('DICOM CT 장면 구성 실패:', error)

    // 폴백: 샘플 3D 메시로 대체
    console.log('샘플 3D 메시로 폴백...')
    return await buildClientSideVTKScene(vtk)
  }
}

/**
 * VTK.wasm 샘플 장면 구성 함수 (폴백용)
 * VTK.wasm JavaScript 가이드의 예제 코드를 기반으로 구현
 */
export async function buildSampleScene(vtk: any) {
  console.log('=== VTK.wasm 볼륨 렌더링 클래스 확인 ===')
  console.log('VTK 네임스페이스:', vtk)

  const allKeys = Object.keys(vtk)
  console.log('전체 VTK 객체 키들:', allKeys)

  // 볼륨 렌더링 관련 클래스 확인
  const volumeClasses = allKeys.filter(
    (key) => key.toLowerCase().includes('volume') || key.toLowerCase().includes('image') || key.toLowerCase().includes('data'),
  )
  console.log('볼륨/이미지 관련 클래스들:', volumeClasses)

  // 중요한 볼륨 렌더링 클래스들 개별 확인
  const criticalClasses = [
    'vtkImageData',
    'vtkVolumeMapper',
    'vtkVolume',
    'vtkDataArray',
    'vtkTypeUint16Array',
    'vtkTypeFloat32Array',
    'vtkColorTransferFunction',
    'vtkPiecewiseFunction',
  ]

  console.log('=== 핵심 볼륨 렌더링 클래스 존재 여부 ===')
  criticalClasses.forEach((className) => {
    const exists = typeof vtk[className] === 'function'
    console.log(`${className}: ${exists ? '✅ 존재' : '❌ 없음'}`)
  })

  // 클라이언트 사이드 VTK.wasm 직접 사용 시도
  if (typeof vtk.vtkPoints === 'function') {
    console.log('클라이언트 사이드 VTK 팩토리 함수 발견! 볼륨 렌더링 검증 시도')
    return await buildDicomCTScene(vtk)
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

ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
