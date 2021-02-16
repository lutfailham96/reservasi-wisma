-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 16, 2021 at 08:49 AM
-- Server version: 10.5.8-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wisma`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar`
--

CREATE TABLE `kamar` (
  `id` int(11) NOT NULL,
  `nama_kamar` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_kelas_kamar` int(11) NOT NULL,
  `kondisi` tinyint(1) NOT NULL COMMENT '0: kosong, 1: dibooking, 2: kotor, 4: rusak',
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `kamar`
--

INSERT INTO `kamar` (`id`, `nama_kamar`, `id_kelas_kamar`, `kondisi`, `created`, `updated`) VALUES
(105, 'B11', 123, 0, '2020-05-19 08:36:48', '2020-05-19 10:07:56');

-- --------------------------------------------------------

--
-- Table structure for table `kelas_kamar`
--

CREATE TABLE `kelas_kamar` (
  `id` int(11) NOT NULL,
  `nama_kelas` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_wisma` int(11) NOT NULL,
  `harga_kelas` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `kelas_kamar`
--

INSERT INTO `kelas_kamar` (`id`, `nama_kelas`, `id_wisma`, `harga_kelas`, `created`, `updated`) VALUES
(123, 'VIP', 1, 350000, '2020-05-19 08:36:11', '2020-05-19 08:36:11'),
(124, 'Standard', 2, 200000, '2020-05-19 08:36:24', '2020-05-19 08:36:24'),
(125, 'Lobi', 3, 500000, '2020-05-19 08:36:36', '2020-05-19 08:36:36');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id` int(11) NOT NULL,
  `nama_konsumen` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alamat_konsumen` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `kontak_konsumen` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tgl_booking` datetime NOT NULL,
  `tgl_awal` datetime NOT NULL,
  `tgl_akhir` datetime NOT NULL,
  `id_kelas` int(11) NOT NULL,
  `id_kamar` int(11) DEFAULT NULL,
  `nominal` int(11) DEFAULT NULL,
  `tgl_bayar` datetime DEFAULT NULL,
  `status_lunas` tinyint(1) DEFAULT NULL COMMENT '0: pending, 1: lunas',
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id`, `nama_konsumen`, `alamat_konsumen`, `kontak_konsumen`, `tgl_booking`, `tgl_awal`, `tgl_akhir`, `id_kelas`, `id_kamar`, `nominal`, `tgl_bayar`, `status_lunas`, `created`, `updated`) VALUES
(6, 'Lutfa Ilham', 'Cepu', '08798475985252', '2020-05-14 15:26:56', '2020-05-14 04:28:00', '2020-05-15 23:59:00', 15, NULL, NULL, NULL, 0, '2020-05-14 15:28:51', '2020-05-14 15:28:51'),
(7, 'Aui', 'Cepu', '087678928674', '2020-05-14 15:32:02', '2020-05-14 00:00:00', '2020-05-22 23:59:00', 16, NULL, NULL, NULL, 0, '2020-05-14 15:38:36', '2020-05-14 15:38:36'),
(8, 'dfsdfas', 'efsaf', 'wefafadf', '2020-05-14 15:32:02', '2020-05-15 00:00:00', '2020-05-23 23:59:00', 12, NULL, NULL, NULL, 0, '2020-05-14 15:40:02', '2020-05-14 15:40:02'),
(9, 'sdfsdf', 'sdfasdf', 'sdfsadf', '2020-05-14 15:47:14', '2020-05-14 15:47:00', '2020-05-15 23:59:00', 16, NULL, NULL, NULL, 0, '2020-05-14 15:47:40', '2020-05-14 15:47:40'),
(10, 'Usdkjfsdl', 'Blora', '08988556766767', '2020-05-14 15:47:14', '2020-05-14 00:20:00', '2020-05-15 23:59:00', 10, NULL, NULL, NULL, 0, '2020-05-14 15:59:00', '2020-05-14 15:59:00'),
(11, 'sdfadsf', 'sdfasd', 'sdfasdf', '2020-05-14 16:10:54', '2020-05-14 14:00:00', '2020-05-15 00:00:00', 16, NULL, NULL, NULL, 0, '2020-05-14 16:10:55', '2020-05-14 16:10:55'),
(12, 'Lutfa Ilham', 'Cepu', '0888888888', '2020-05-15 08:34:34', '2020-05-15 14:00:00', '2020-05-30 12:00:00', 16, NULL, NULL, NULL, 0, '2020-05-15 10:24:08', '2020-05-15 10:24:08'),
(13, 'sdlfkjdsl', 'asdfjoiejwaf', '567769087342', '2020-05-15 16:09:13', '2020-05-15 14:00:00', '2020-05-23 12:00:00', 16, NULL, NULL, NULL, 0, '2020-05-15 16:09:34', '2020-05-15 16:09:34');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jabatan` tinyint(1) NOT NULL COMMENT '0: admin, 1: operator',
  `status` tinyint(1) NOT NULL COMMENT '0: nonaktif, 1: aktif',
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `nama`, `jabatan`, `status`, `created`, `updated`) VALUES
(1, 'admin', 'pbkdf2:sha256:150000$WRn5RqhN$b2c47f00139951dc709d7cc4b8f9ad01ded8b03492171e5180fecc6d26cd0d4f', 'Admin Wisma', 0, 1, '0000-00-00 00:00:00', '2020-05-12 11:44:13'),
(2, 'operator', 'pbkdf2:sha256:150000$OTKmTJ46$2b539668071c11fa95e64435a3fb05edde8a53ea8a88260e7973733c1e61786c', 'Operator', 1, 1, '0000-00-00 00:00:00', '2020-05-19 10:09:21'),
(3, 'resepsionis', 'pbkdf2:sha256:150000$hUN44OdT$d9d3a5ec1c94ac84640ef797e9b62fa817d5c6fc91bce707777bb6d1724e9df7', 'Resepsi', 1, 1, '2020-05-12 12:06:13', '2020-05-18 16:07:35'),
(4, 'lutfailham', 'pbkdf2:sha256:150000$Lthkhual$d0c85bfcdb5670ad4087ba3c2a38cfac4f9020c2cb234a8ca7521bcce8dca1d0', 'Lutfa Ilham', 0, 1, '2020-05-13 16:17:48', '2020-05-28 08:09:03');

-- --------------------------------------------------------

--
-- Table structure for table `wisma`
--

CREATE TABLE `wisma` (
  `id` int(11) NOT NULL,
  `nama_wisma` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alamat_wisma` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_telp` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `wisma`
--

INSERT INTO `wisma` (`id`, `nama_wisma`, `alamat_wisma`, `no_telp`, `created`, `updated`) VALUES
(1, 'Wisma Widya Patra III', 'Jl. Olah Raga No.1, Kampungbaru, Karangboyo, Kec. Cepu, Kabupaten Blora, Jawa Tengah 58315', '(0296) 421888', '0000-00-00 00:00:00', '2020-05-17 18:11:33'),
(2, 'Wisma Nglajo II', 'Jl. Plaju Nglajo, Wonotejo, Cepu, Kec. Cepu, Kabupaten Blora, Jawa Tengah 58112', '(0296) 421888', '2020-05-12 15:44:33', '2020-05-12 15:44:33'),
(3, 'Wisma Nglajo I', 'Jl. Plaju No.14A, Wonotejo, Cepu, Kec. Cepu, Kabupaten Blora, Jawa Tengah 58112', '(0296) 421888', '2020-05-12 16:21:39', '2020-05-18 15:17:22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kelas_kamar`
--
ALTER TABLE `kelas_kamar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `wisma`
--
ALTER TABLE `wisma`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kamar`
--
ALTER TABLE `kamar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=108;

--
-- AUTO_INCREMENT for table `kelas_kamar`
--
ALTER TABLE `kelas_kamar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `wisma`
--
ALTER TABLE `wisma`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
