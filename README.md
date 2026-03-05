<div align="center">

# 🤖 4-Link Planar Robot Kinematics Simulation

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/BesliPakpahan/Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange.svg)](https://github.com/BesliPakpahan/Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics/issues)

**Author: BESLI SAUT MARITO PAKPAHAN**  
*SEMS6 - Legged Robot Course | March 2026*

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

</div>

---

<a name="english"></a>

## 📖 English Version

### 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Demos & Animations](#demos--animations)
- [Robot Configuration](#robot-configuration)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Simulation Details](#simulation-details)
- [Mathematics](#mathematics)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

### 🔍 Overview

A comprehensive simulation suite for a 4-link planar robot arm, featuring:
- **Forward Kinematics (FK)**: Calculate end-effector position from joint angles
- **Inverse Kinematics (IK)**: Two methods (Analytical & CCD)
- **Trajectory Following**: Follow complex 2D paths
- **Workspace Analysis**: Visualize reachable workspace
- **High-Quality Visualizations**: Animations and plots with 200 DPI resolution

### ✨ Features

- ✅ **Forward Kinematics** - Direct computation from joint angles to end-effector position
- ✅ **Inverse Kinematics** - Two methods available:
  - Analytical solution for 2-link equivalent
  - Cyclic Coordinate Descent (CCD) for full 4-DOF control
- ✅ **Advanced Trajectory Following** - Follow complex paths:
  - Circles, Spirals, Hearts, Stars, Infinity symbols, Sine waves
- ✅ **Workspace Analysis** - Visualize and analyze reachable workspace
- ✅ **Rich Visualizations** - High-quality animations (200 DPI images, 4000 bitrate videos)
- ✅ **Video Export** - Save simulations as MP4 videos and GIF animations
- ✅ **Interactive Jupyter Notebook** - Experiment with the robot interactively

### 🎥 Demos & Animations

#### Forward Kinematics - All Joints Moving
![Forward Kinematics Animation](outputs/gifs/fk_animation_all_joints.gif)

#### Inverse Kinematics - Circle Trajectory
![IK Circle Animation](outputs/gifs/ik_animation_circle.gif)

#### Trajectory Following - Heart Shape
![Heart Trajectory](outputs/gifs/trajectory_heart.gif)

#### Trajectory Following - Spiral Pattern
![Spiral Trajectory](outputs/gifs/trajectory_spiral.gif)

#### Trajectory Following - Star Pattern
![Star Trajectory](outputs/gifs/trajectory_star.gif)

### 🤖 Robot Configuration

The robot consists of 4 links with the following default lengths:

| Link | Length |
|------|--------|
| Link 1 | 1.0 m |
| Link 2 | 1.0 m |
| Link 3 | 0.8 m |
| Link 4 | 0.6 m |

**Total Maximum Reach**: 3.4 m

### 🚀 Installation

#### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video generation)

#### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**  
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

#### Install Python Dependencies

1. Clone this repository:
```bash
git clone https://github.com/BesliPakpahan/Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics.git
cd Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### 💻 Usage

#### Option 1: Run All Simulations
```bash
python run_all_simulations.py
```

#### Option 2: Run Individual Simulations
```bash
# Simulation 1: Forward Kinematics
python simulation_1_forward_kinematics.py

# Simulation 2: Inverse Kinematics
python simulation_2_inverse_kinematics.py

# Simulation 3: Trajectory Following
python simulation_3_trajectory.py

# Simulation 4: Workspace Analysis
python simulation_4_workspace.py
```

#### Option 3: Interactive Jupyter Notebook
```bash
jupyter notebook interactive_demo.ipynb
```

### 📁 Project Structure

```
PLANAR_KINEMATIC/
├── 📄 kinematics.py                        # Core kinematics module (FK & IK)
├── 📄 visualizer.py                        # Visualization and animation utilities
├── 📄 simulation_1_forward_kinematics.py   # Forward kinematics demo
├── 📄 simulation_2_inverse_kinematics.py   # Inverse kinematics demo
├── 📄 simulation_3_trajectory.py           # Trajectory following demo
├── 📄 simulation_4_workspace.py            # Workspace analysis
├── 📄 run_all_simulations.py               # Run all simulations
├── 📓 interactive_demo.ipynb               # Jupyter notebook for interactive use
├── 📋 requirements.txt                     # Python dependencies
├── 📖 README.md                            # This file
├── 📝 QUALITY_IMPROVEMENTS.md              # Quality improvements log
└── 📁 outputs/                             # Generated videos and images
    ├── 📁 gifs/                            # GIF animations (auto-play on GitHub)
    ├── 🖼️ fk_*.png                         # Forward kinematics images
    ├── 🎬 fk_*.mp4                         # Forward kinematics videos
    ├── 🖼️ ik_*.png                         # Inverse kinematics images
    ├── 🎬 ik_*.mp4                         # Inverse kinematics videos
    ├── 🎬 trajectory_*.mp4                 # Trajectory following videos
    └── 🖼️ workspace_*.png                  # Workspace analysis images
```

### 🔬 Simulation Details

#### Simulation 1: Forward Kinematics
Demonstrates how joint angles affect the end-effector position.

**Outputs:**
- 6 static configuration snapshots
- 1 comparison plot
- 4 animation videos (joint rotation, all joints, wave, joint space)

**Key Concepts:**
- Direct computation from joint angles to position
- Joint space exploration
- Configuration comparison

#### Simulation 2: Inverse Kinematics
Shows how to reach target positions using two IK methods.

**Outputs:**
- Analytical IK snapshots and comparison
- CCD-based solutions and comparison
- 4 animation videos (circle, figure-8, square, multi-target)

**Key Concepts:**
- Analytical IK (2-link equivalent)
- Cyclic Coordinate Descent (CCD)
- Redundancy resolution
- Path following

#### Simulation 3: Trajectory Following
Demonstrates following complex trajectories.

**Outputs:**
- 5 trajectory animations (spiral, heart, star, infinity, sine wave)
- 1 comparison plot

**Key Concepts:**
- Smooth trajectory generation
- Continuous IK solving
- Path planning

#### Simulation 4: Workspace Analysis
Analyzes the robot's reachable workspace.

**Outputs:**
- Random sampling visualization
- Systematic sampling visualization
- Density heatmap
- Boundary detection (convex hull)
- Workspace exploration animation
- Statistics text file

**Key Concepts:**
- Workspace characterization
- Reachability analysis
- Density distribution
- Configuration space sampling

### 📐 Mathematics

#### Forward Kinematics

Given joint angles θ₁, θ₂, θ₃, θ₄, the end-effector position is:

```
x = L₁cos(θ₁) + L₂cos(θ₁+θ₂) + L₃cos(θ₁+θ₂+θ₃) + L₄cos(θ₁+θ₂+θ₃+θ₄)
y = L₁sin(θ₁) + L₂sin(θ₁+θ₂) + L₃sin(θ₁+θ₂+θ₃) + L₄sin(θ₁+θ₂+θ₃+θ₄)
```

#### Inverse Kinematics

**Method 1: Analytical**
- Fixes θ₃ and θ₄
- Solves 2-link IK for θ₁ and θ₂
- Fast but limited flexibility

**Method 2: CCD (Cyclic Coordinate Descent)**
- Iteratively adjusts each joint to minimize error
- Handles full 4-DOF control
- More flexible but slower

### 🎨 Customization

#### Modify Robot Configuration
```python
link_lengths = [1.0, 1.0, 0.8, 0.6]  # [L1, L2, L3, L4]
robot = PlanarRobot4Link(link_lengths)
```

#### Create Custom Trajectories
```python
def generate_custom_path(n_points=200):
    path = []
    for i in range(n_points):
        t = (2 * np.pi * i) / n_points
        x = # your x equation
        y = # your y equation
        path.append([x, y])
    return np.array(path)
```

#### Adjust Animation Parameters
```python
viz.animate_trajectory(
    angles_sequence,
    filename='my_animation.mp4',
    fps=30,                    # Frames per second
    show_trajectory=True,      # Show trajectory trail
    show_workspace=True        # Show workspace boundaries
)
```

### 🐛 Troubleshooting

**FFmpeg Not Found**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

**Memory Issues**
- Reduce `n_frames` in simulation scripts
- Reduce `n_samples` in workspace analysis
- Run simulations individually

**Animation Not Saving**
- Check disk space
- Ensure `outputs/` directory exists
- Try saving as GIF instead of MP4

### 📊 Performance

Typical execution times (Intel i7, 16GB RAM):
- Simulation 1: ~2.6 minutes
- Simulation 2: ~3.7 minutes
- Simulation 3: ~5.3 minutes
- Simulation 4: ~1.1 minutes

**Total: ~12.8 minutes for all simulations**

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🙏 Acknowledgments

- Planar kinematics concepts from robotics textbooks
- Visualization inspired by modern robotics libraries
- CCD algorithm implementation based on research papers

### 📧 Contact

**BESLI SAUT MARITO PAKPAHAN**  
SEMS6 - Legged Robot Course

For questions or issues, please create an issue in the repository.

---

<a name="bahasa-indonesia"></a>

## 📖 Versi Bahasa Indonesia

### 📋 Daftar Isi
- [Ringkasan](#ringkasan)
- [Fitur](#fitur-id)
- [Demo & Animasi](#demo--animasi)
- [Konfigurasi Robot](#konfigurasi-robot)
- [Instalasi](#instalasi-id)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Detail Simulasi](#detail-simulasi)
- [Matematika](#matematika-id)
- [Kustomisasi](#kustomisasi)
- [Pemecahan Masalah](#pemecahan-masalah)
- [Lisensi](#lisensi-id)

---

### 🔍 Ringkasan

Suite simulasi komprehensif untuk lengan robot planar 4-link, dengan fitur:
- **Forward Kinematics (FK)**: Hitung posisi end-effector dari sudut joint
- **Inverse Kinematics (IK)**: Dua metode (Analitis & CCD)
- **Trajectory Following**: Ikuti jalur 2D yang kompleks
- **Analisis Workspace**: Visualisasi workspace yang dapat dijangkau
- **Visualisasi Berkualitas Tinggi**: Animasi dan plot dengan resolusi 200 DPI

### ✨ Fitur {#fitur-id}

- ✅ **Forward Kinematics** - Komputasi langsung dari sudut joint ke posisi end-effector
- ✅ **Inverse Kinematics** - Dua metode tersedia:
  - Solusi analitis untuk ekuivalen 2-link
  - Cyclic Coordinate Descent (CCD) untuk kontrol 4-DOF penuh
- ✅ **Trajectory Following Lanjutan** - Ikuti jalur kompleks:
  - Lingkaran, Spiral, Hati, Bintang, Simbol Infinity, Gelombang Sinus
- ✅ **Analisis Workspace** - Visualisasi dan analisis workspace yang dapat dijangkau
- ✅ **Visualisasi Kaya** - Animasi berkualitas tinggi (gambar 200 DPI, video bitrate 4000)
- ✅ **Export Video** - Simpan simulasi sebagai video MP4 dan animasi GIF
- ✅ **Jupyter Notebook Interaktif** - Eksperimen dengan robot secara interaktif

### 🎥 Demo & Animasi

#### Forward Kinematics - Semua Joint Bergerak
![Forward Kinematics Animation](outputs/gifs/fk_animation_all_joints.gif)

#### Inverse Kinematics - Trajektori Lingkaran
![IK Circle Animation](outputs/gifs/ik_animation_circle.gif)

#### Trajectory Following - Bentuk Hati
![Heart Trajectory](outputs/gifs/trajectory_heart.gif)

#### Trajectory Following - Pola Spiral
![Spiral Trajectory](outputs/gifs/trajectory_spiral.gif)

#### Trajectory Following - Pola Bintang
![Star Trajectory](outputs/gifs/trajectory_star.gif)

### 🤖 Konfigurasi Robot

Robot terdiri dari 4 link dengan panjang default sebagai berikut:

| Link | Panjang |
|------|---------|
| Link 1 | 1.0 m |
| Link 2 | 1.0 m |
| Link 3 | 0.8 m |
| Link 4 | 0.6 m |

**Total Jangkauan Maksimum**: 3.4 m

### 🚀 Instalasi {#instalasi-id}

#### Prasyarat
- Python 3.8 atau lebih tinggi
- FFmpeg (untuk pembuatan video)

#### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**  
Download dari [ffmpeg.org](https://ffmpeg.org/download.html)

#### Install Dependensi Python

1. Clone repository ini:
```bash
git clone https://github.com/BesliPakpahan/Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics.git
cd Planar-Kinematics-Inverse-Kinematics-Forward-Kinematics
```

2. Install paket yang diperlukan:
```bash
pip install -r requirements.txt
```

### 💻 Cara Penggunaan

#### Opsi 1: Jalankan Semua Simulasi
```bash
python run_all_simulations.py
```

#### Opsi 2: Jalankan Simulasi Individual
```bash
# Simulasi 1: Forward Kinematics
python simulation_1_forward_kinematics.py

# Simulasi 2: Inverse Kinematics
python simulation_2_inverse_kinematics.py

# Simulasi 3: Trajectory Following
python simulation_3_trajectory.py

# Simulasi 4: Analisis Workspace
python simulation_4_workspace.py
```

#### Opsi 3: Jupyter Notebook Interaktif
```bash
jupyter notebook interactive_demo.ipynb
```

### 📁 Struktur Proyek

```
PLANAR_KINEMATIC/
├── 📄 kinematics.py                        # Modul kinematics inti (FK & IK)
├── 📄 visualizer.py                        # Utilitas visualisasi dan animasi
├── 📄 simulation_1_forward_kinematics.py   # Demo forward kinematics
├── 📄 simulation_2_inverse_kinematics.py   # Demo inverse kinematics
├── 📄 simulation_3_trajectory.py           # Demo trajectory following
├── 📄 simulation_4_workspace.py            # Analisis workspace
├── 📄 run_all_simulations.py               # Jalankan semua simulasi
├── 📓 interactive_demo.ipynb               # Jupyter notebook untuk penggunaan interaktif
├── 📋 requirements.txt                     # Dependensi Python
├── 📖 README.md                            # File ini
├── 📝 QUALITY_IMPROVEMENTS.md              # Log peningkatan kualitas
└── 📁 outputs/                             # Video dan gambar yang dihasilkan
    ├── 📁 gifs/                            # Animasi GIF (auto-play di GitHub)
    ├── 🖼️ fk_*.png                         # Gambar forward kinematics
    ├── 🎬 fk_*.mp4                         # Video forward kinematics
    ├── 🖼️ ik_*.png                         # Gambar inverse kinematics
    ├── 🎬 ik_*.mp4                         # Video inverse kinematics
    ├── 🎬 trajectory_*.mp4                 # Video trajectory following
    └── 🖼️ workspace_*.png                  # Gambar analisis workspace
```

### 🔬 Detail Simulasi

#### Simulasi 1: Forward Kinematics
Mendemonstrasikan bagaimana sudut joint mempengaruhi posisi end-effector.

**Output:**
- 6 snapshot konfigurasi statis
- 1 plot perbandingan
- 4 video animasi (rotasi joint, semua joint, wave, joint space)

**Konsep Kunci:**
- Komputasi langsung dari sudut joint ke posisi
- Eksplorasi joint space
- Perbandingan konfigurasi

#### Simulasi 2: Inverse Kinematics
Menunjukkan cara mencapai posisi target menggunakan dua metode IK.

**Output:**
- Snapshot dan perbandingan IK analitis
- Solusi berbasis CCD dan perbandingan
- 4 video animasi (circle, figure-8, square, multi-target)

**Konsep Kunci:**
- IK Analitis (ekuivalen 2-link)
- Cyclic Coordinate Descent (CCD)
- Resolusi redundansi
- Path following

#### Simulasi 3: Trajectory Following
Mendemonstrasikan mengikuti trajektori kompleks.

**Output:**
- 5 animasi trajektori (spiral, hati, bintang, infinity, sine wave)
- 1 plot perbandingan

**Konsep Kunci:**
- Generasi trajektori halus
- Penyelesaian IK kontinyu
- Perencanaan jalur

#### Simulasi 4: Analisis Workspace
Menganalisis workspace yang dapat dijangkau robot.

**Output:**
- Visualisasi sampling acak
- Visualisasi sampling sistematis
- Heatmap densitas
- Deteksi batas (convex hull)
- Animasi eksplorasi workspace
- File teks statistik

**Konsep Kunci:**
- Karakterisasi workspace
- Analisis keterjangkauan
- Distribusi densitas
- Sampling configuration space

### 📐 Matematika {#matematika-id}

#### Forward Kinematics

Diberikan sudut joint θ₁, θ₂, θ₃, θ₄, posisi end-effector adalah:

```
x = L₁cos(θ₁) + L₂cos(θ₁+θ₂) + L₃cos(θ₁+θ₂+θ₃) + L₄cos(θ₁+θ₂+θ₃+θ₄)
y = L₁sin(θ₁) + L₂sin(θ₁+θ₂) + L₃sin(θ₁+θ₂+θ₃) + L₄sin(θ₁+θ₂+θ₃+θ₄)
```

#### Inverse Kinematics

**Metode 1: Analitis**
- Menetapkan θ₃ dan θ₄
- Menyelesaikan IK 2-link untuk θ₁ dan θ₂
- Cepat tetapi fleksibilitas terbatas

**Metode 2: CCD (Cyclic Coordinate Descent)**
- Secara iteratif menyesuaikan setiap joint untuk meminimalkan error
- Menangani kontrol 4-DOF penuh
- Lebih fleksibel tetapi lebih lambat

### 🎨 Kustomisasi

#### Modifikasi Konfigurasi Robot
```python
link_lengths = [1.0, 1.0, 0.8, 0.6]  # [L1, L2, L3, L4]
robot = PlanarRobot4Link(link_lengths)
```

#### Buat Trajektori Kustom
```python
def generate_custom_path(n_points=200):
    path = []
    for i in range(n_points):
        t = (2 * np.pi * i) / n_points
        x = # persamaan x Anda
        y = # persamaan y Anda
        path.append([x, y])
    return np.array(path)
```

#### Sesuaikan Parameter Animasi
```python
viz.animate_trajectory(
    angles_sequence,
    filename='my_animation.mp4',
    fps=30,                    # Frame per detik
    show_trajectory=True,      # Tampilkan jejak trajektori
    show_workspace=True        # Tampilkan batas workspace
)
```

### 🐛 Pemecahan Masalah

**FFmpeg Tidak Ditemukan**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

**Masalah Memori**
- Kurangi `n_frames` di script simulasi
- Kurangi `n_samples` di analisis workspace
- Jalankan simulasi secara individual

**Animasi Tidak Tersimpan**
- Periksa ruang disk
- Pastikan direktori `outputs/` ada
- Coba simpan sebagai GIF alih-alih MP4

### 📊 Performa

Waktu eksekusi tipikal (Intel i7, 16GB RAM):
- Simulasi 1: ~2.6 menit
- Simulasi 2: ~3.7 menit
- Simulasi 3: ~5.3 menit
- Simulasi 4: ~1.1 menit

**Total: ~12.8 menit untuk semua simulasi**

### 📄 Lisensi {#lisensi-id}

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

### 🙏 Penghargaan

- Konsep planar kinematics dari buku teks robotika
- Visualisasi terinspirasi dari library robotika modern
- Implementasi algoritma CCD berdasarkan makalah penelitian

### 📧 Kontak

**BESLI SAUT MARITO PAKPAHAN**  
SEMS6 - Legged Robot Course

Untuk pertanyaan atau masalah, silakan buat issue di repository.

---

<div align="center">

### ⭐ Jika proyek ini berguna, berikan star!

Made with ❤️ for Robotics Education

</div>
