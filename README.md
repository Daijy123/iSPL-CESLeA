# iSPL CESLeA Project
[![license]](/LICENSE)[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

---

<!--- Short introduction -->
This is a repository for ISPL's turnkey project on Behavioral Prediction (인식예측). We use IMU sensor data collected from standalone sensor devices, smartphones, smartwatches and other on-body gadgets to learn a user's behaviour and predict their patterns.

Conventional Human Activity Recognition Systems rely on Statistical Machine Learning techniques to extract features from raw data so as to identify human activities. Our system utilizes Deep Learning to identify 3 human activities and also identifies the indoor location of a user in real-time using raw data obtained from an IMU sensor strapped to the waist of a user.
(기존의 인간 활동 인식 시스템들은 사람의 활동을 식별하기 위해 원시 데이터에서 형상을 추출하기 위해 통계 기계 학습 기법에 의존한다. 저희시스템은 딥러닝을 활용해 3가지 인간 활동을 파악하고, 사용자의 허리에 묶인 IMU 센서에서 얻은 원시 데이터를 이용해 사용자의 실내 위치를 실시간으로 파악한다.)
적용분야: Application is usable as a part of other systems that require knowing what activity a user is currently performing and the location of the user in an indoor environment (사용자가 현재 어떤 활동을 수행하고 있는지, 실내 환경에서 사용자의 위치를 알아야 하는 다른 시스템의 일부로 애플리케이션을 사용할 수 있음)

The server.py part of this application continuously collects data from a sensor that is strapped to a user's waist. It computes the user's current indoor location that is stored in a file. At the same time, it processes and windows accelerometer and gyroscope data that is stored in a file. 
(이 어플리케이션의 server.py 부분은 사용자의 허리에 묶인 센서로부터 지속적으로 데이터를 수집한다. 파일에 저장된 사용자의 현재 실내 위치를 계산한다. 동시에 파일에 저장된 윈도우 가속도계와 자이로스코프 데이터를 처리한다.)
The run_model.py part uses the windowed sensor data from the file it is stored in to continuously make predictions using a pre-trained model. These predictions are displayed in the display model generated by the display.py script. This script also displays the user's current position in x and y coordinates.
(run_model.py 부분은 미리 훈련된 모델을 사용하여 지속적으로 예측하기 위해 저장된 파일의 윈도우 센서 데이터를 사용한다. 이러한 예측은 display.py 스크립트에 의해 생성된 디스플레이 모델에 표시된다. 또한 이 스크립트는 사용자의 현재 위치를 x 좌표와 y 좌표로 표시한다.)
The locationPlotter.py script continuously displays (plots) the user's current indoor location coordinate and a view of the entire trajectory as well can be seen.
(locationPlotter.py 스크립트는 사용자의 현재 실내 위치 좌표를 지속적으로 표시(표시)하고 전체 궤적을 볼 수 있다.)

This project is currently under development.
[README for Korean / 한국어 도움말]

**Table of Contents**

- [Key Features](#key-features)
- [Installation](#installation)
- [Introduction](#introduction)
- [Contribution guidelines](#contribution-guidelines)
- [LICENSE](#license)

## Key Features

<!---
- Super Great Feature
- Wow! awesome!
- Make sure that each features is written in one line. **Key** Features!
- '-' will make this listed.
-->

## Installation

<!---
Write the way how to use this module.
YOU MUST CHECK THIS ONCE on your additional hardware.
-->

## Contribution guidelines

If you want to contribute to this software, be sure to review the [contribution guidelines]. This project adheres to the [code of conduct]. By participating, you are expected to uphold this code.

## Introduction

Check [Introduction file] to read full version. This is summary.

<b>[Autonomous Digital Companion]</b> is a research project generalized by [KETI] (Korea Electronics Technnology Institute), supported by the [IITP] (Institute for Information & Communications Technology Promotion) grant funded by the [Ministry of Science and ICT] (MSIT, a ministry of the Government of South Korea). This is a fundamental study for designing companions who provide the help you need for daily life. They also help you manage a better life and they respond to you out of sympathy because they understand your thoughts and intentions.

<b>[CESLeA]</b> is the third detailed project of Autonomous Digital Companion. It is an intelligent interaction technology research and development project that analyzes multi-modal data with AI learning techniques to grasp environment and user's state. It also interprets it with context-aware information including contextual understanding.

<!---
Write short introduction of your module.
DONT WRITE TOO MUCH. README is manual not historical textbook.
If you wanna make some links, use [blahblah] and look below.
-->
## Citation
- A. Poulose and D. S. Han, "UWB Indoor Localization Using Deep Learning LSTM Networks," Applied Sciences, vol. 10, pp. 6290, 2020.
- A. Poulose and D. S. Han, "Hybrid Indoor Localization Using IMU sensor and Smartphone Camera," Sensors, vol. 19, pp. 5084, 2019.
- A. Poulose, J. Kim, and D. S. Han, “A Sensor Fusion Framework for Indoor Localization Using Smartphone Sensors and Wi-Fi RSSI Measurements," Applied Sciences, vol. 9, pp. 4379, 2019.
- A. Poulose, B. Senouci and D. S. Han, "Performance Analysis of Sensor Fusion Techniques For Heading Estimation Using Smartphone Sensors," IEEE Sensors Journal, vol. 19, no. 24, pp. 12369-12380, 2019.
- A. Poulose, O. S. Eyobu, and D. S. Han, “An Indoor Position-Estimation Algorithm Using Smartphone IMU Sensor Data," IEEE Access, vol. 7, pp. 11165-11177, 2019.
  
## LICENSE

[version 3 of the GNU Lesser General Public License]

<!---
Here is for making links. if you used [blahblah] above this section, Here you can make them hypertext.
You need to change the destination of each urls to your own repository.
-->
[README for Korean / 한국어 도움말]: https://github.com/rmutegeki/iSPL-CESLeA/blob/master/README_ko.md
[license]: https://img.shields.io/github/license/Katinor/CESLeA_readme_template
[contribution guidelines]: https://github.com/rmutegeki/iSPL-CESLeA/blob/master/CONTRIBUTING.md
[code of conduct]: https://github.com/rmutegeki/iSPL-CESLeA/blob/master/CODE_OF_CONDUCT.md
[Introduction file]: https://github.com/rmutegeki/iSPL-CESLeA/blob/master/INTRO.md
[Autonomous Digital Companion]: http://aicompanion.or.kr/
[KETI]: https://www.keti.re.kr/
[Ministry of Science and ICT]: https://www.msit.go.kr/
[IITP]: https://www.iitp.kr/
[CESLeA]: http://abr.knu.ac.kr/wordpress/ceslea/
[version 3 of the GNU Lesser General Public License]: https://github.com/rmutegeki/iSPL-CESLeA/blob/master/LICENSE
