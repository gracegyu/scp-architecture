# Y-IndexedDB 조사

## 개요

- <https://github.com/yjs/y-indexeddb>
- IndexedDB 데이터베이스 어댑터를 사용하여 공유 데이터를 브라우저에지속적으로 저장
- 다음에 세션에 참여할 때 변경 사항은 그대로 유지
- 서버와 클라이언트 간에 교환되는 데이터의 양을 최소화
- 오프라인 편집이 가능

## 사용법

### 연결

IndexeddbPersistence 함수를 이용해서 ydoc을 indexeddb에 연결해주면 됨

```javascript
const ydoc = new Y.Doc()

const provider = new WebsocketProvider(`ws://y-websocket.esclouddev.com`, id, ydoc)

provider.on('status', (event) => {
  console.log('provider:status', event.status)
})

const dbProvider = new IndexeddbPersistence(id, ydoc)

dbProvider.on('synced', () => {
  console.log('content from the database is loaded')
})
```

### 연결 끊기

```javascript
dbProvider.destroy()
```

### indexedDB 비우기

```javascript
dbProvider.clearData()
```

## 실험

- Offline 상태에서 Web client에서 수정 후 Web browser 종료 후 재시작

  - 수정한 내용이 그대로 남아 있다.

- 다시 online 상태로 바꾸면 y-websocket 서버와 sync되어서 모든 client와 sync된다.
  - 이 때 indexedDB의 데이터가 삭제되는지는 알아내지 못했다.
  - Ydoc 데이터는 모두 indexedDB에 저장되는 것인지? Sync가 안된 데이터만 저장되는 것인지 알 수 없음. 아마 모두 저장되는 것으로 추측됨

## IndexedDB 조회

- 크롬 > Inspect > Application > Storage > IndexedDB에서 조회 가능
- Uint8Array로 저장되어 있어서 내용을 알 수는 없다.
