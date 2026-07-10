# 1.1 Switch to Section Layout
CT 실행 후 Section Layout으로 전환할 수 있다.

1.**Layout 선택 버튼**

a.CT 실행 시 기본 layout은 MPR이다.

①[MPR], [Section] 버튼은 토글 버튼으로, MPR ↔ Section layout 간 전환된다.

②현재 활성화된 layout에 따라 [MPR], [Section] 버튼이 토글된다.


# 1.2 Section Layout Overview
Section Layout 구성 설명

1.**Scout View의 구성**

a.Curve가 입력된 단면이 표시되는 영역

①Axial 단면이 default로 표시된다.

–MPR 레이아웃의 default 위치와 동일하게 적용한다.

–단, MPR 레이아웃의 Axial 단면과 연동되지 않는다.

b.영상 정보 표시

①좌측 상단에는 Patient 정보가 표시된다.

②우측 상단에는 Width/Level값과 Filter가 표시된다.

③화면 상단에는 R, L이 표시된다.

④우측 하단에는 thickness, interval, total slice 정보가 표시된다.

⑤우측 중앙에는 스케일바(ruler)가 표시된다.

c.Curve

①Curve를 등록/관리할 수 있는 버튼이 표시된다.

d.Slider

①Scout view의 slice를 변경할 수 있는 slider가 표시된다.

②Slice에는 H(Head, 머리 방향)와 F(Foot, 발 방향)가 표시된다.

e.Image Adjust/Setting/최대화

①동작 방식은 MPR 레이아웃과 동일하다.

- 

2.**Panorama View의 구성**

a.입력된 Curve를 기준으로 구성된 Panorama가 표시되는 영역

b.영상 정보 표시

①우측 상단에는 Width/Level값과 Filter가 표시된다.

②화면 상단에는 R, L이 표시된다.

③우측 하단에는 thickness, interval 정보가 표시된다.

c.Slider

①Panorama view의 slice를 변경할 수 있는 slider가 표시된다.

②Slider에는 P(Posterior, 후방)와 A(Anterior, 전방)가 표시된다.

d.Image Adjust/Setting/최대화

①동작 방식은 MPR 레이아웃과 동일하다.

- 

3.**Section View의 구성**

a.입력된 Curve를 기준으로 단면이 표시되는 영역

b.영상 정보 표시

①좌측 상단에는 slice number가 표시된다.

②우측 상단에는 Width/Level값과 Filter가 표시된다.

③화면 상단에는 B(Buccal), L(Lingual)이 표시된다.

–Scout view에 표시되는 Section Line의 B/L 방향 표시와 동일한 방향으로 표시된다.

④Section view에는 가로, 세로에 스케일바(ruler)가 표시되고, 스케일바(ruler)는 단면의 확대/축소 배율에 따라 실시간으로 업데이트된다.

–Section slice의 가로/세로축 전체에 스케일바(ruler)가 표시된다. (PoC와 상이함, PoC에서는 영상 폭에 맞춰 스케일바(ruler)가 표시됨)

c.Slider

①Section view의 slice를 변경할 수 있는 slider가 표시된다.

②Slider에는 R과 L이 표시된다.

d.Image Adjust/Setting/최대화

①동작 방식은 MPR 레이아웃과 동일하다.

# 1.3 Scout View Curve Components
Scout View의 Curve 구성 요소 설명

**구성 요소의 명칭 및 정의는 본 페이지에서 설명하며, 각 요소의 동작 방식은 [EP01_F007_ScoutView]를 참고한다.**

- 

1.**Curve**

a.Scout view 상에 Draw Curve 모드에서 그려진 점을 spline으로 구현한 curve

- 

2.**Section line**

a.Section view의 interval에 따라 curve를 slice한 line

b.Section view에서 넘겨볼 수 있는 모든 slice의 위치를 표시한다.

c.그림상에서 curve의 시작부터 끝지점까지 수직으로 그려진 빨간색 선을 의미한다.

- 

3.**Active section line**

a.Section view (3x3)에서 표시되는 9개의 slice를 표시하는 line

①V1.3.2에서는 Section view를 9개로 고정한다.

–Section view 개수를 변경할 수 없다.

②Section view에 표시되는 영상의 가로 폭을 시각적으로 표시하며, Active section line의 길이는 Section view의 가로 폭과 동일하다.

–EP01_F007_ScoutView의 2번 항목 참고

–Section view 가로 폭의 default 길이는 30mm이다.

b.기본 위치는 Section Line의 중간 지점이다.

c.그림상에서 curve에 수직으로 그려진 9개의 빨간색 긴 선을 의미한다.

- 

4.**Center section line**

a.Section view에서 5번째 (중앙)에 위치하는 slice를 표시하는 line

①Section line과 다른 색상으로 표시된다.

b.Active section line의 중앙 노란색 선을 의미하며, control point가 있다.

- 

5.**Panorama navigator line**

a.Panorama view에서 표시되는 panorama slice의 위치를 나타내는 line

①Default 위치는 curve line과 동일하다.

b.Panorama view에서 slice 변경 시 Panorama slice의 위치가 표시된다.

c.그림상에서 curve를 offset한 하나의 초록색 선을 의미한다.

- 

6.**Panorama thickness line**

a.Panorama View에 설정된 thickness 범위를 나타내는 line

b.그림상에서 curve를 offset한 한 쌍의 초록색 line, control point가 있다.

7.**L/B 방향 표시**

a.B/L방향: B(Buccal)는 치아의 협측(바깥쪽), L(Lingual) 은 설측(혀쪽)을 의미한다.

b.Curve 입력 시에 방향이 결정되며, 해당 로직은 Ez3D-i와 동일하게 처리한다.

①Ez3D-i에 구현된 코드 재사용 가능한지 개발실 확인 후 스펙 확정

②[EP01_F005_DrawCurve]의 3번 항목과 동일하다.

c.그림상에서 curve의 양 끝에 표시된 하얀색 text를 의미한다.

- 

8.**BL/LB 기준점**

a.draw curve 시 첫 번째로 입력한 Point 위치에 생성된다.

b.BL/LB 기준점은 삼각형 아이콘과 BL/LB text로 구성된다.

c.이 삼각형 아이콘의 위치를 기준으로 Section view의 B와 L 표기 방향이 결정된다

①Active Section Line의 중간을 지나면 BL/LB 기준점을 중심으로 Section slice의 B/L 표기가 반전된다. (이미지 참고)

d.삼각형 아이콘 이동에 따라 Section View가 실시간으로 업데이트된다.

e.그림상에서 curve의 시작점에 위치한 연두색 삼각형을 의미한다.


# 1.4 Panorama View Line Components
Panorama View의 Line 구성 요소 설명

**구성 요소의 명칭 및 정의는 본 페이지에서 설명하며, 각 요소의 동작 방식은 [EP01_F008_PanoView]를 참고한다.**

1.**파노라마 이미지 경계선**

a.파노라마 이미지의 상하 경계선을 표시하는 line이다. (노란색 가로 실선)

b.두 경계선 사이의 Default 거리는 100mm이다.

- 

2.**파노라마 이미지의 중심선**

a.파노라마 이미지, Seciton 이미지의 중심 선이다. (초록색 가로 실선)

- 

3.**Scout 이미지 위치선**

a.Scout 이미지의 현재 위치를 표시하는 선이다. (흰색 가로 점선)

b.Default 위치는 파노라마 이미지의 중심선과 동일하다.

- 

4.**Active section line**

a.Panorama view상에 Section view의 Active section line의 위치를 표시한다.

①그 중 가운데 위치한 Center section line은 다른 색상으로 표시된다.


# 1.5 Draw Curve
Scout view에서 커브를 입력할 수 있다.

1.**[Draw Curve] 버튼**

a.Curve를 등록/관리할 수 있는 버튼이 표시되는 영역으로, curve가 존재하지 않을 시에는 [Draw Curve] 버튼이, curve가 존재할 시에는 curve 번호와 [편집], [삭제] 버튼이 위치한다.

b.[Draw Curve] 버튼 클릭 시, [Draw Curve] 버튼이 토글되며, Scout 영역 내에서 마우스 커서가 변경된다.

①[Draw Curve] 버튼은 토글 방식으로 동작한다.

②클릭 시 Draw Curve 모드 진입, 다시 클릭 시 Draw Curve 모드가 종료된다.

–이때, 작성 중이던 curve는 반영되지 않고 Draw Curve 모드가 종료된다.

- 

2.**Curve를 구성하는 Point 입력**

a.Scout view에서 원하는 지점을 연속으로 클릭하여 curve를 입력한다.

①Point 입력에 따라 spline으로 point들이 연결되며 curve line이 생성된다.

②Point 입력 중 마우스 커서를 이동하면, 마지막으로 입력된 Point에서 현재 커서 위치까지의 curve가 실시간으로 미리보기된다.

③미리보기 중인 curve를 기준으로 Section line, Active section line이 Scout view에 실시간으로 업데이트된다. (PoC에서는 2점 찍힌 이후에는 Active section line의 위치는 업데이트 하지 않음. 개발실 리뷰 후 스펙 확정)

–Draw curve 모드에서 Active section line은 항상 section line의 중간 지점에 위치한다.

b.마우스 좌클릭 시에는 point가 입력되고, 우클릭 시에는 직전에 입력한 point가 입력 취소된다.

①단, point가 하나만 존재할 시에는 우클릭 하여도 입력 취소가 되지 않는다.

c.Draw curve 모드에서 [ESC] 버튼 클릭 시, draw curve 모드가 종료된다.

d.마지막 지점 입력 시, 더블 클릭하여 curve 입력을 종료한다.

3.**L/B 방향 표시**

a.Curve 입력 시에 방향이 결정되며, 해당 로직은 Ez3D-i와 동일하게 처리한다.

①Ez3D-i에 구현된 코드 재사용 가능한지 개발실 확인 후 스펙 확정

4.**입력된 Curve를 기준으로 Panorama 및 Section View 생성**

a.Section view

①Curve point 입력에 따라 section line이 생성되면, 이에 맞춰 Section view가 표시된다. (PoC와 상이함)

–Curve 입력 완료 전까지는 Section view는 blank 상태이다.

b.Panorama view

①Curve 입력이 완료되면, curve Line을 따라 구성된 파노라마 영상이 Panorama view에 표시된다.

–Curve 입력 완료 전까지는 Panorama view는 blank 상태이다.

–

5.**Draw Curve 모드 중 동작 지원 여부**

a.UI disabled / 정상 동작 유지 기능 목록 → MMI 말미의 Appendix. 모드별 동작 지원 여부 페이지를 참고한다.

b.커서 disabled 처리:

①입력이 불가한 Panorama, Section view 영역(title영역은 제외)에서는 disabled 커서가 표시되며, 다른 동작을 수행할 수 없다.


# 1.6 Edit Curve
Curve 및 Point를 편집할 수 있다.

1.**Curve 편집**

a.Scout 헤더의 [Edit Curve] 버튼을 클릭하여 curve 편집 모드로 진입한다.

①[Edit Curve] 버튼은 토글 방식으로 동작한다.

②클릭 시 편집 모드 진입, 다시 클릭 시 편집 모드가 종료된다.

- 

2.**Curve 전체 이동**

a.편집모드에서 Curve 위에 마우스 커서 hover하면 마우스 커서 형태가 변경되고, drag&drop하여 curve 전체를 이동시킬 수 있다.

- 

3.**Curve point 위치 이동**

a.편집모드에서 point 위에 마우스 커서 hover하면 마우스 커서 형태가 변경되고, drag&drop하여 각 point를 이동시킬 수 있다.

①Drag 하려고 클릭하는 시점에 점이 선택된다.

②Drop 시점에 선택 해제된다.

③Drop 시점에 Curve가 업데이트되고, 이에 맞춰 Panorama view, Section view가 업데이트된다.

b.Curve 시작점/ 종료점을 비롯한 모든 Curve line을 수정 할 수 있다.

c.Curve 위치 조정에 제한은 없으며, Curve Point Order에 따라 Spline으로 연결하여 업데이트 한다.

- 

4.**Curve Point 삭제**

a.편집 모드에서 Curve의 point 위에서 context menu를 실행한다.

b.Context menu에서 [Delete Point]를 선택하면 해당 point가 삭제된다.

①포인트가 삭제되면 이전 포인트와 이후 포인트가 Spline 방식으로 연결되어 업데이트 된다.

②Curve의 시작 포인트와 종료 포인트도 삭제할 수 있으며, 삭제되는 경우 포인트를 제외한 상태로 Curve가 업데이트 된다.

c.Curve를 구성하는 최소 Point 개수(2개)일 경우에는 point를 삭제할 수 없다.

①Context menu 실행이 불가하다.

- 

5.**Curve Point 추가**

a.Curve 위의 point가 존재하지 않는 지점에서 context menu를 실행한다.

b.Context menu에서 [Add Point]를 선택하면 해당 위치에 새로운 Point가 추가된다.

①추가된 Point는 전후 포인트 Order의 사이의 순번을 가진다.

- 

6.**Curve 삭제**

a.Scout 헤더의 [Delete Curve] 버튼을 클릭하거나, curve 위의 point가 존재하지 않는 지점에서 context menu를 실행하여 [Delete Curve]를 선택한다.

b.위 동작 실행 시 Curve 삭제 여부를 확인하는 message box가 표시된다.

①[Message]: Curve를 삭제하시겠습니까?

②[확인] 클릭 시, Curve가 삭제되고 Panorama 및 Section View는 초기 상태로 전환된다.

③[취소] 클릭 시, message box가 표시 해제된다.

c.Curve 삭제 시, Panorama View 및 Section View가 초기 상태로 전환된다.

- 
7.**L/B 방향 전환**

a.Curve 위의 point가 존재하지 않는 지점에서 context menu를 실행하여 [L/B Switching]을 선택한다.

b.선택 시 Scout, Section view에 표시된 B/L 텍스트가 서로 반전되어 표시된다.  (B↔L)

①Section View에 표시되는 B/L 텍스트도 동일하게 반전되어 표시된다.

②단, 영상 자체의 flip(반전)은 발생하지 않으며, 텍스트 표시만 변경된다.

- 

8.**BL/LB 기준점 위치 이동 (PoC에 없음, 개발실 리뷰 후 적용 여부 확정)**

a.BL/LB 기준점 위에 마우스를 hover하면 마우스 커서가 변경된다.

b.BL/LB 기준점을 drag & drop하여 위치를 이동할 수 있다.

①BL/LB 기준점은 Curve 상의 Section line을 따라 한 칸씩 이동한다.

- 

9.**수정된 Point/Curve를 기준으로 Panorama 및 Section View 업데이트**

a.Point 이동, 추가, 삭제 등 Curve가 변경되는 모든 동작 시점에 Panorama view 및 Section view가 실시간으로 업데이트된다.

b.Curve의 경우, 변경된 Point 기준으로 Section line, Active section line의 위치가 재계산되어 표시된다.

①Point가 이동/추가/삭제될 경우, Active section line은 항상 Section line의 중앙으로 위치하도록 업데이트된다.

- 

10.**Edit Curve 모드 중 동작 지원 여부**

a.UI disabled / 정상 동작 유지 기능 목록 → MMI 말미의 Appendix. 모드별 동작 지원 여부 페이지를 참고한다.

b.커서 disabled 처리

①입력이 불가한 Panorama, Section view 영역(title영역은 제외)에서는 disabled 커서가 표시되며, 다른 동작을 수행할 수 없다.

②단, Panorama, Section view에서 마우스 휠 & slider를 통한 slice 이동은 가능하다.


# 1.7 Scout View Controls
Scout view에서 사용 가능한 조작 기능 설명

**Scout view에서 사용 가능한 조작 기능에 대한 설명이다.**

**단, 별도 설명이 필요하지 않은 공통 기능은 [EP01_F013_CommonTools]를 참고한다.**

- 

1.**Active section line 위치 이동**

a.Active section line위에 마우스를 hover하면 마우스 커서가 변경된다.

b.Active section line을 drag & drop하여 위치를 이동할 수 있다.

①Active section line은 curve에 표시된 section line을 따라 이동한다.

②이동된 Active section line의 위치에 맞춰 Section view의 slice가 업데이트된다.

③Active section line 위치 변경에 따라 Panorama view의 Active section line이 업데이트된다.

- 

2.**Active section line 길이 조절**

a.Center section line 양 끝에 위치한 control point에 마우스를 hover하면 마우스 커서가 변경된다.

b.Center section line의 control point를 drag & drop하여 Active section line의 길이와 Section view에 표시되는 영상의 가로 폭을 조절할 수 있다. (PoC와 상이함, PoC에서는 Slider 를 이용)

①한 쪽의 point를 조정하면 반대편의 point가 대칭으로 함께 조정된다.

3.**Panorama thickness 조절**

a.Panorama thickness line의 control point를 drag & drop하여 Panorama View의 thickness를 조절할 수 있다.

①조정 시 Panorama View의 thickness가 실시간으로 업데이트된다.

②한 쪽의 line을 조정하면 반대편의 line이 대칭으로 함께 조정된다.

b.Curve에서 thickness를 조정한 경우, Panorama view의 우측 하단의 thickness overlay와 setting dialog에 thickness값이 반영된다.

①단, setting dialog에서 thickness를 클릭하면 콤보박스가 표시되는데, curve에서 조정한 thickness값이 콤보박스의 선택 항목에 없을 경우 콤보박스에는 선택 값이 표시되지 않고, select value에만 해당 값이 표시된다.

4.**Scout view의 slice 변경**

a.Scout View에서 마우스 휠을 사용거나 slider를 이동하여 Scout 이미지의 slice를 변경할 수 있다.

b.Scout 이미지 위치 변경 시 Panorama view의 Scout 이미지 위치선(흰색 점선)이 실시간으로 업데이트된다.

①Panorama view의 Scout 위치선은 Scout view를 통해서만 조작이 가능하며, Panorama view상에서의 조작은 지원하지 않는다.

5.**Curve 삭제**

a.Curve 상에서 context menu를 실행하여 curve를 삭제할 수 있다.

①편집 모드에서와 동일하게 동작한다.

- 

6.**L/B 방향 전환**

a.Curve 상에서 context menu를 실행하여 L/B 방향을 전환할 수 있다.

①편집 모드에서와 동일하게 동작한다.

- 

7.**BL/LB 기준점 위치 이동 (PoC에 없음, 개발실 리뷰 후 적용 여부 확정)**

a.BL/LB 기준점을 이동하여 Section slice의 B, L 방향의 기준점을 설정할 수 있다.

①편집 모드에서와 동일하게 동작한다.

# 1.8 Panorama View Controls
Panorama view에서 사용 가능한 조작 기능 설명

**일반 모드의 Panorama view에서 사용 가능한 조작 기능에 대한 설명이다.**

**단, 별도 설명이 필요하지 않은 공통 기능은 [EP01_F013_CommonTools]를 참고한다.**

- 

1.**파노라마 이미지 경계선 (노란색 가로 실선) 이동**

a.Line 위에 마우스를 hover하면 마우스 커서가 변경된다.

b.Line을 drag & drop하여 Section 영상의 세로 폭을 조정할 수 있다. (PoC와 상이함, PoC에서는 Slider를 이용)

c.양 쪽이 대칭으로 한 번에 움직인다.

①대칭 중심점은 파노라마 이미지 중심선이다.

- 

2.**파노라마 이미지 중심선 (초록색 가로 실선) 이동**

a.Line 위에 마우스를 hover하면 마우스 커서가 변경된다.

b.Drag & drop하여 위치를 이동할 수 있다.

c.Drop 시점에 Scout, Panorama, Section view가 갱신된다.

①이동된 line의 위치가 Panorama, Section view의 중심일 수 있게 각 단면 view가 업데이트된다.

②Drop 시점에 Scout 이미지 위치선(흰색 점선)이 파노라마 이미지 중심선과 동일하게 업데이트된다.

- 

3.**Active section line (초록색 세로 실선) 위치 이동**

a.Active section line 위에 마우스를 hover하면 마우스 커서가 변경된다.

b.Active section line을 drag & drop하여 위치를 이동할 수 있다.

c.Active section line의 위치에 맞춰 Section view의 slice가 업데이트된다.

d.Active section line 위치 변경에 따라 Scout view의 Active section line이 업데이트된다.

- 

4.~~**Active section line (초록색 세로 실선) 각도 변경 (PoC에 없음, 적용 여부 결정 필요)**~~

**[v1.3.2 스펙아웃]** Clever Space CT viewer 임플란트 시뮬레이션 탑재 시점에 재검토 (PLAN-1287 #3, 2026-07-09 기획 확정)

~~a.Center Section Line 양 끝에 위치한 control point에 마우스를 hover하면 마우스 커서가 변경된다.~~

~~b.Control point를 drag & drop하여 Active section line의 각도를 회전시킬 수 있다.~~

~~①회전 시, 변경된 Active section line에 따라 Section view가 구성된다.~~

~~②회전 시, 파노라마 이미지의 중심선과 만나는 점을 중심으로 회전된다.~~

~~③회전 시 control point는 파노라마 이미지 경계선을 따라 이동한다.~~

~~c.회전하면 해당 각도를 반영하여 Section View가 업데이트된다.~~

~~d.단, Scout View상의 Section Line은 업데이트되지 않는다.~~

~~e.각도는 ±45도 범위 내에서 조절 가능하다.~~

~~①이때, 파노라마 이미지의 경계선을 이동하여도 각도는 변경되지 않는다.~~

- 

5.**Panorama View의 slice 변경**

a.마우스 휠을 사용하거나 slider를 이동하여 Panorama 이미지의 slice를 변경할 수 있다.

b.Panorama slice 변경 시 Scout view의 Panorama navigator line이 실시간으로 업데이트된다.

①Scout View의 Panorama navigator line은 Panorama view를 통해서만 조작이 가능하며, Scout View상에서의 조작은 지원하지 않는다.

-

# 1.9 Section View Controls
Section view에서 사용 가능한 조작 기능 설명

**일반 모드의 Section view에서 사용 가능한 조작 기능에 대한 설명이다.**

**단, 별도 설명이 필요하지 않은 공통 기능은 [EP01_F013_CommonTools]를 참고한다.**

- 

1.**Section view의 slice 변경**

a.마우스 휠을 사용하거나 slider를 이동하여 Section 이미지의 slice를 변경할 수 있다.

b.Slice 변경 시 Section view 좌측 상단의 slice number가 실시간으로 업데이트된다.

c.Section view에서 slice를 변경하면 Scout view 및 Panorama view의 Active section line 위치가 실시간으로 업데이트된다.

- 

2.**Center slice 표시**

a.9개 영상 중 5번째(중앙)가 Center section line에 해당하는 slice이며, 타이틀에 별도 표시*가 된다.

①별도 표시: 슬라이스 번호를 bold 처리하는 등의 강조 표시 방식은 GUI styleguide를 참고한다.

- 

3.**최대화**

a.Section view에서 최대화 기능 사용 시, 3x3 그리드 레이아웃은 그대로 유지되며, 전체 화면 크기에 맞게 확장되어 표시된다.

b.Section view에서 각 slice를 더블클릭할 시, 개별 slice를 최대화할 수 있다. (Ez3D-i 지원 기능, 개발실 리뷰 후 적용 여부 확정)


# 1.10 Thickness and Interval Settings
Section 레이아웃의 Thickness 및 Interval을 변경할 수 있다.

**Thickness/ Interval**

단면 영상의 두께와 단면 간격을 조정하는 기능

1.**[Setting] Button**

a.2D View Title Bar에 있는 [Setting] 버튼

①Thickness와 Interval 옵션값을 조절할 수 있다.

b.제공되는 Thickness/Interval 옵션값은 모든 단면 영상에서 동일하며, 기능 동작 방식도 MPR 레이아웃과 동일하다.

- 

2.**Thickness/Interval default 값**

a.Scout view

①Thickness: 0mm

②Interval: Voxel Based Interval

③Scout View는 MPR 속성의 View이므로 MPR 서브모듈의 단면 view와 Thickness/Interval 값이 상호 동기화된다.

b.Panorama view

①Thickness: 0mm

②Interval: 1mm

c.Section view

①Thickness: 0mm

②Interval: 1mm

- 

3.**Thickness/Interval 변경**

a.선택한 View의 Thickness/Interval 값이 변경된다.

①Scout, Panorama, Section view에서 각기 다르게 적용된다.

②각 view의 Image Information Overlay에 Thickness, Interval 값이 함께 업데이트 된다.

③Scout view에서 Interval 값 변경 시에는 Total Slice overlay가 함께 업데이트 된다.

④각 단면 view의 Interval값에 따라 Slider의 slice 정보도 업데이트된다.

b.일반 모드와 Draw curve 모드에서 Section view의 Interval 조정 시, 변경된 Interval에 맞춰 Scout View와 Panorama view의 Section line, Active section line의 간격이 업데이트 되며, Active section line은 Section line의 중간 지점으로 위치하도록 업데이트된다.

c.Draw curve 모드에서 Scout view의 Thickness/Interval 조정 시, 진행 중이던 Draw curve가 취소될 수 있다. (개발실 리뷰 후 스펙 확정)

①MPR 레이아웃에서 Angle 측정 중 Thickness/Interval 변경 시 기능이 취소되는 동작처럼 Draw curve 기능 실행이 취소되어도 무방하다.


# 1.11 Windowing and Image Filter
Section View의 Windowing 값을 변경하고 Image Filter를 적용할 수 있다.

1.**[Image Adjust] Button**

a.2D View Title Bar에 있는 [Image Adjust] 버튼을 클릭하여 각 단면 view의 image filter를 적용한다.

①영상의 Width, Level 값을 변경하고 Smooth, Sharpen, Max Sharpen, Inverse, MIP 필터를 적용 및 초기화할 수 있다.

②모든 단면에 한 번에 적용되며, Windowing값과 Filter 적용 여부가 view의 좌측 상단에 text로 표시된다.

b.MPR 레이아웃과 연동

①Image Adjust 의 default값은 MPR 레이아웃과 동일하다.

②Image Adjust에서 조정한 Windowing값이나 Filter는 MPR 레이아웃의 단면 view와 연동된다.


# 1.12 Additional Common Tools
공통 툴 신규 추가 (Angle 순서 변경, Free Draw 기능 확대, Arrow 신규 추가)

1.**[Angle] 버튼 순서 변경**

a.Measurement 도구(Length, Angle)와 Annotation 도구(Free Draw, Arrow)를 각각 인접하게 배치하기 위해 Angle 버튼을 Length 버튼 우측으로 이동한다.

- 

2.**[Free Draw] 기능 적용 확대**

a.MPR 레이아웃, Section 레이아웃의 2D 단면 view에 모두 [Free Draw] 기능을 추가한다. (3D View에는 적용되지 않는다.)

b.단, [Arrow] 툴과 동일하게 각 단면별로 입력 가능하다.

- 

3.**[Arrow] 툴 신규 추가**

a.MPR 레이아웃, Section 레이아웃의 2D 단면 view에 모두 적용되는 Arrow 툴을 추가한다. (3D View에는 적용되지 않는다.)

b.Arrow 툴 동작 방식

①첫 번째 클릭 시 시작점(화살표 머리가 없는 쪽)이 찍힌다.

②두 번째 클릭 시 끝점(화살표 머리/삼각형이 있는 쪽)이 찍히며 입력이 완료된다.

③Arrow는 각 영역(View) 단위로만 입력 가능하다.

–Scout View, Panorama View는 각각 해당 영역 안에서만 입력 가능하다.

–Section View는 각 slice 안에서만 입력 가능하며, 다른 slice로 넘어갈 수 없다.

- 
-

# 1.13 Section Layout Common Tools
Section 레이아웃에서 Cloud Web Viewer의 공통 툴을 사용할 수 있다.

**Section 레이아웃에서 사용 가능한 공통 툴에 대한 설명이다.**

**공통 툴의 동작 방식은 MPR 레이아웃과 동일하게 적용한다.**

1.**Top tool bar 도구 (MPR 레이아웃과 동일하게 동작)**

a.Pan, Zoom, Reset View, Pointer

b.Length, Angle, Free Draw, Arrow

①단, 각 section별로 동작한다. (section slice 경계를 넘나들 수 없음)

- 

2.**화면 표시 제어**

a.Show/Hide Grid

b.Show/Hide Overlay

- 

3.**작업 관리**

a.Reset Cloud Work

b.Initialize All

- 

4.**레이아웃 전환**

a.Single/Dual Layout 전환

b.View Original

- 

5.**영상 조정**

a.Image Adjust, Setting (Thickness, Interval 조정), 최대화

 
6.**계측, 주석 Overlay 표시 규칙 (Clever One 코드 기반 기준)**
  1. 계측, 주석 Overlay 귀속 기준
     1. Scout/Panorama/Section view의 Overlay는 Curve 및 생성 시점의 평면에 귀속된다.
        - 평면은 생성 시점의 point와 normal로 정의된다.
        - V1.3.2에는 단일 Curve 생성을 지원하지만, 차기 버전에서 입력 가능한 curve 개수가 증가할 수 있음을 염두할 필요가 있다.
  2. Section view Overlay 표시 조건
     1. 현재 표시 중인 슬라이스 평면과 Overlay 생성 시점의 평면을 비교하여, 아래 두 조건을 모두 만족하는 경우 해당 Overlay를 표시한다.
     2. 거리 오차: 현재 슬라이스 평면으로부터 저장된 interval의 ±Interval/2 범위 이내
     3. 방향 오차(Normal): 실사용에 불편하지 않은 수준으로 별도 정의
  3. Curve Point 변경 시
     1. 각 Section slice의 Normal이 변경되므로, normal의 판정 오차에 의해 기존 Overlay가 표시되지 않을 수 있다.
     2. 단, Overlay 데이터가 삭제되는 것은 아니며, 생성 시점과 동일한 평면 조건이 충족되면 다시 표시된다.
  4. Interval 변경 시
     1.  Normal은 유지되므로, 원래 위치로 이동하면 기존 Overlay 확인이 가능하다.
  5.  Thickness 변경 시
      1.  Thickness 변경 시 Overlay 표시 조건에는 영향을 주지 않는다.
  6.  Overlay는 MPR 레이아웃과 공유되지 않는다.

# 1.14 Save Project
Section 레이아웃의 작업 내용을 저장할 수 있다.

1.**Cloud Web Viewer 작업 내용 저장 기능**

a.MPR 레이아웃과 동일한 방식으로 작업 내용을 prj 파일에 저장한다.

b.Section 레이아웃 고유 항목(Curve, Panorama 관련 설정 등) 외 공통 저장 항목은 MPR 레이아웃과 동일하게 적용한다.

c.(참고) 저장 대상 항목은 아래와 같다.

①마지막으로 선택한 레이아웃 (MPR / Section)

②각 단면 View의 위치 (Scout, Panorama, Section View의 slice 위치 및 Active section line 위치)

③각 단면 View의 카메라 상태 (Position, Panning 등)

④ShowGrid 표시 여부

⑤Section Curve (Point 좌표 포함)

⑥Panorama View의 가로선 위치 (파노라마 이미지 경계선 위치)

⑦Panorama View의 중심선 위치

⑧각 단면의 Thickness / Interval 설정값

⑨각 단면의 Overlay 입력값 (Length, Angle, Arrow, Free Draw 등)

⑩각 단면의 Windowing / Image Filter 설정값

⑪B/L Switching 상태

⑫BL/LB 기준점 위치

(~~⑧Active Section Line의 회전 각도~~ — v1.3.2 미적용·스펙아웃, PLAN-1287 #3)

d.단, 상기 항목은 개발실 리뷰 후 변경될 수 있다.

- 

2.**저장된 prj 파일 기반으로 CT 재오픈**

a.동일한 CT를 다시 열 경우, 마지막으로 저장된 prj 파일을 기준으로 작업 환경이 복원된다.

b.마지막 저장 시 선택된 레이아웃(MPR 또는 Section)으로 오픈된다.

c.Section 레이아웃으로 오픈될 경우, 저장된 Curve를 기준으로 Panorama 및 Section View가 설정된다.

-

# Appendix. 1. 모드별 동작 지원 여부 

| **툴/기능** | **일반 모드** | **Draw Curve 모드** | **Edit Curve 모드** |
| --- | --- | --- | --- |
| **Top Tool Bar 공통 툴** |  |  |  |
| Pan / Zoom / Reset View / Pointer | ● | ✕ | ✕ |
| Length / Angle 측정 | ● | ✕ | ✕ |
| Free Draw / Arrow | ● | ✕ | ✕ |
| Show/Hide Patient Information | ✕ (MPR과 동일) | ✕ | ✕ |
| Show/Hide Grid, Show/Hide Overlay | ● | ● | ● |
| Reset Cloud Work / Initialize All | ● | ✕ | ✕ |
| **네비게이션 / 기타** |  |  |  |
| LNB, 상단 Back 버튼 등 Clever Space의 viewer외 메뉴 | ● | ● (클릭 시 변경사항 저장 없이 이동) | ● (클릭 시 변경사항 저장 없이 이동) |
| View Original | ● | ✕ (UI disabled) | ✕ (UI disabled) |
| Single/Dual Layout 전환 | ● (MPR과 동일) | ● | ● |
| **Scout View** |  |  |  |
| Image Adjust (Width/Level 조정 / Image Filter) / 최대화 | ● | ● | ● |
| Setting (Thickness / Interval 조정) | ● | ● | ● |
| Slice 이동 (마우스 휠 / Slider) | ● | ● | ● |
| Active section line 조정 (길이 조절, 위치 이동) | ● | ✕ (클릭은 point 입력으로만 동작) | ● |
| Panorama thickness line 조절 | ● | ✕ (클릭은 point 입력으로만 동작) | ● |
| Curve point 조정 (생성, 이동, 삭제) | ✕ | △ (point 생성) | ● (point 생성, 이동, 삭제) |
| Curve 조정 (이동, 삭제) | △ (curve 삭제) | ✕ (클릭은 point 입력으로만 동작) | ● (curve 이동, 삭제) |
| L/B switching | ● | ✕ (우클릭 시 직전 point 취소) | ● |
| BL/LB 기준점 이동 | ● | ✕ (클릭은 point 입력으로만 동작) | ● |
| **Panorama View** |  |  |  |
| Image Adjust (Width/Level 조정 / Image Filter) / 최대화 | ● | ✕ (UI disabled) | ● |
| Setting (Thickness / Interval 조정) | ● | ✕ (UI disabled) | ● |
| Slice 이동 (마우스 휠 / Slider) | ● | ✕ (UI disabled) | ● |
| Panorama 이미지 경계선 이동 | ● | ✕ (화면 blank) | ● |
| Panorama 이미지 중심선 이동 | ● | ✕ (화면 blank) | ● |
| Active section line 위치 이동 | ● | ✕ (화면 blank) | ● |
| ~~Active section line 각도 회전 (±45°)~~ | — (v1.3.2 스펙아웃) | — | — |
| **Section View** |  |  |  |
| Image Adjust (Width/Level 조정 / Image Filter) / 최대화 | ● | ✕ (UI disabled) | ● |
| Setting (Thickness / Interval 조정) | ● | ✕ (UI disabled) | ● |
| Slice 이동 (마우스 휠 / Slider) | ● | ✕ (UI disabled) | ● |



