# 방 청결도 분석 서비스
사용자가 웹 페이지에서 촬용한 방 사진을 AI가 분석하여 청결 상태를 판단하고 점수로 제공하는 서비스
## 📌 프로젝트 개요
- 수행 기간 : 2026.03.06 ~ 2026.03.09
- 팀원 : 김병현, 김권, 김동석
- 주요 기능 :
  - 웹 서버를 통해 AI 모델 제공
  - 웹 인터페이스를 통해 카메라 촬영
  - 사용자가 촬영한 방 사진을 AI가 분석하여 방의 청결도 판단
  - 분석 결과를 기반으로 방의 청결도를 점수로 제공
- 이미지 데이터 : https://drive.google.com/file/d/1zRa7_d0KYaFIF0zut54_O40gkiUf1IgI/view?usp=drive_link
## 🔧 기술 스택
| 기술 | 설명 |
|----------|------------|
| Python | 전체 시스템 및 AI 모델 개발 |
| Pytorch, TensorFlow| 이미지를 학습하여 청결도를 분류하는 딥러닝 모델 학습 |
| CUDA | 딥러닝 모델 학습 속도 향상을 위한 GPU 연산 사용 |
| OpenCV | 이미지 로드, 크기 조정, 전처리 수행 |
| Flask | AI 모델을 제공하는 웹 서버 실행 |

<h2>🛠 개발 환경 (Development Environment)</h2>

<table width="100%">
<tr>
<td width="50%" valign="top">

<h3>🔧 Hardware</h3>

<b>PLC 시스템</b><br>
- Mitsubishi Q03UDV (Q-Series)<br>
- Q-Series Base Unit<br><br>

<b>I/O 및 모션 모듈</b><br>
- 디지털 입력 : QX40<br>
- 디지털 출력 : QY10<br>
- 아날로그 입출력 : Q64AD2DA<br>
- 위치결정 모듈 : QD77MS2<br><br>

<b>모션 제어 시스템</b><br>
- 서보 앰프 : MR-J4-10B<br>
- 서보 모터 : HG-KR13J<br>
- 1축 볼스크류 구동 구조<br><br>

<b>공압 시스템</b><br>
- 공급 / 가공 / 스토퍼 / 흡착 실린더 적용<br><br>

<b>센서</b><br>
- 근접 센서 : CR18-8DN<br>
- 금속 감지 센서 : PRL18-8DN<br>

</td>

<td width="50%" valign="top">

<h3>💻 Software</h3>

<b>PLC 프로그래밍</b><br>
- GX Works2 (v1.631H)<br><br>

<b>서보 파라미터 설정</b><br>
- MR Configurator2 (v1.165X)<br><br>

<b>HMI 설계</b><br>
- GT Designer3 (v1.2565)<br><br>

<b>제어 로직 구현</b><br>
- Ladder Logic 기반 제어 프로그램 설계<br>
- 위치 제어 및 모션 제어 통합 구성<br>

</td>
</tr>
</table>

<h2>⚙ 서보모터 구성 및 설정 (Servo Motor Configuration)</h2>

<h3>Basic Parameters 1</h3>

- Movement amount per rotation : **10000 μm**

<h3>Basic Parameters 2</h3>

- Speed limit value : **3000 mm/min**  
- Acceleration time 0 : **500 ms**  
- Deceleration time 0 : **500 ms**

<h3>Detailed Parameters 2</h3>

- Acceleration time 1 : **200 ms**  
- Acceleration time 2 : **500 ms**  
- Deceleration time 1 : **200 ms**  
- Deceleration time 2 : **500 ms**  
- JOG speed limit value : **3000 mm/min**

<h3>HPR Basic Parameters</h3>

- HPR direction : **Reverse direction**  
- HPR speed : **1500 mm/min**  
- Creep speed : **80 mm/min**  
- HPR retry : **Retry HPR with limit switch**

<h3>System Configuration</h3>

PLC → 위치결정모듈 → 서보앰프 → 서보모터 → 서보앰프 (Feedback)

## 🔎 구현 상세
### 1️⃣ 선입 선출
- 선입
  - 금속 센서와 비금속 센서의 신호가 ON되면 적재 층 카운트, 적재 수량 카운트를 1 증가
  - 적재 층 카운트에 따라 설정된 층에 소재 적재
  - 센서 인식 내부 릴레이를 통해 창고의 전/후진 여부 결정
  - 적재 층 카운트 3에 도달하면 카운트 초기화
  - 적재 수량 카운트 3에 도달하면 이후 들어오는 소재 배출
- 선출
  - 출고 윈도우에 출고 횟수 설정, 설정된 횟수만큼 동작
  - 출고 횟수에 따라 출고 층 카운트 1 증가, 적재 수량 카운트 1 감소
  - 출고 층 카운트 3에 도달하면 카운트 초기화
  - 적재 수량 카운트 0이라면 작동 X
### 2️⃣ 상태점점
  - 층별 상태 점검 버튼 존재
  - 선입 동작 중 각 창고 위치 학습(티칭)
  - 상태 점검 버튼 누르면 해당 층 소재 출고
  - 소재 공급 후 동작 버튼 누르면 출고된 층에 다시 적재
### 3️⃣ 안전설계
- 비상 정지 회로
  - 비상 버튼을 누르면 모든 동작 중지, 흡착 모터는 계속 작동
  - 화면에 나오는 윈도우를 통해 재가동과 초기화 선택 가능
- 후진완료 릴레이
  - 전원 ON과 동작 완료 이후 모든 실린더가 후진완료되어있지 않다면 후진 신호 ON
  - 모든 실린더가 후진되었다면 서보 모터 원점 복귀
- InterLock 회로
  - 선입, 선출, 상태점검 등 각 동작 릴레이에 다른 동작의 릴레이를 B접점
  - 선입이 작동하고 있다면 선출, 상태점검은 버튼을 눌러도 작동하지 않게 됨
