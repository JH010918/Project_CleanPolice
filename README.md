# 방 청결도 분석 서비스
사용자가 웹 페이지에서 촬용한 방 사진을 AI가 분석하여 청결 상태를 판단하고 점수로 제공하는 서비스
## 📌 프로젝트 개요
- 수행 기간 : 2026.03.06 ~ 2026.03.20
- 팀원 : 김병현, 김권, 김동석
- 배경 : 1인 가구 증가에 따라 주거 환경을 관리하는 데 어려움을 겪는 사용자를 위해 사진 한 장으로 방의 청결 상태를 객관적으로 진단하고 정리 지침을 제공하는 서비스
- 주요 기능 :
  - 웹 서버를 통해 AI 모델 제공
  - 이미지 업로드 및 청결도 점수화 (0~100점)
  - Grad-CAM을 이용한 오염/무질서 구역 시각화(히트맵)
  - YOLO 기반의 객체 분포 분석
  - CLIP 기반의 방 상태 요약 제
- 이미지 데이터 : https://drive.google.com/file/d/1zRa7_d0KYaFIF0zut54_O40gkiUf1IgI/view?usp=drive_link
## 🔧 기술 스택
| 기술 | 설명 |
|----------|------------|
| Python | 전체 시스템 및 AI 모델 개발 |
| Pytorch, TensorFlow| 이미지를 학습하여 청결도를 분류하는 딥러닝 모델 학습 |
| CUDA | 딥러닝 모델 학습 속도 향상을 위한 GPU 연산 사용 |
| OpenCV | 이미지 로드, 크기 조정, 전처리 수행 |
| Flask | AI 모델을 제공하는 웹 서버 실행 |
| MYSQL | 청결도 이미지 데이터베이스 관리 |

## 📌 시스템 아키텍처
<img width="725" height="483" alt="system_architecture" src="https://github.com/user-attachments/assets/389489cd-f0d0-499e-b41c-b6e98d15546f" />

## 💾 데이터
### 1️⃣ 수집
- 크롤링
  - Python을 사용한 웹 크롤링을 통해 데이터 수집
### 2️⃣ 전처리
  - 해상도 : 256px * 256px
  - jpg 포맷
  - 사람, 로고 등이 들어가 있는 이미지 제거
### 3️⃣ 라벨링
- clean
- dirty

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


