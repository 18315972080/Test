-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.26 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 book 的数据库结构
DROP DATABASE IF EXISTS `book`;
CREATE DATABASE IF NOT EXISTS `book` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `book`;

-- 导出  表 book.tbl_book 结构
DROP TABLE IF EXISTS `tbl_book`;
CREATE TABLE IF NOT EXISTS `tbl_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '图书id',
  `book` varchar(50) NOT NULL COMMENT '图书名',
  `price` int(11) NOT NULL COMMENT '价格/元',
  `publisher` varchar(50) NOT NULL COMMENT '出版社',
  `author` varchar(50) NOT NULL COMMENT '作者',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '出版时间',
  `cid` int(11) DEFAULT NULL COMMENT '关联tbl_category:图书类别',
  PRIMARY KEY (`id`),
  UNIQUE KEY `book` (`book`),
  KEY `FK_tbl_book_tbl_category` (`cid`),
  CONSTRAINT `FK_tbl_book_tbl_category` FOREIGN KEY (`cid`) REFERENCES `tbl_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  book.tbl_book 的数据：~4 rows (大约)
/*!40000 ALTER TABLE `tbl_book` DISABLE KEYS */;
REPLACE INTO `tbl_book` (`id`, `book`, `price`, `publisher`, `author`, `ctime`, `cid`) VALUES
	(1, '高等数学', 10, '清华社', '张飞', '2026-03-08 22:09:51', 2),
	(2, '英语四级练习册', 20, '外研社', '刘备', '2026-03-08 22:11:09', 1),
	(3, '火影忍者漫画', 10, '火影研究社', '关羽', '2026-03-08 22:11:56', NULL);
/*!40000 ALTER TABLE `tbl_book` ENABLE KEYS */;

-- 导出  表 book.tbl_category 结构
DROP TABLE IF EXISTS `tbl_category`;
CREATE TABLE IF NOT EXISTS `tbl_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '图书类别id',
  `category` varchar(50) NOT NULL COMMENT '图书类别',
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  book.tbl_category 的数据：~4 rows (大约)
/*!40000 ALTER TABLE `tbl_category` DISABLE KEYS */;
REPLACE INTO `tbl_category` (`id`, `category`) VALUES
	(3, '人工智能类'),
	(1, '人文社科类'),
	(2, '自然科学类');
/*!40000 ALTER TABLE `tbl_category` ENABLE KEYS */;

-- 导出  表 book.tbl_order 结构
DROP TABLE IF EXISTS `tbl_order`;
CREATE TABLE IF NOT EXISTS `tbl_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `state` varchar(50) NOT NULL COMMENT '状态[已借出,已售卖,已归还,超时未还]',
  `stime` datetime NOT NULL COMMENT '借售时间',
  `etime` datetime DEFAULT NULL COMMENT '应还时间',
  `bid` int(11) NOT NULL COMMENT '图书名',
  `uid` int(11) NOT NULL COMMENT '关联tbl_user:借售人',
  PRIMARY KEY (`id`),
  KEY `FK_tbl_order_tbl_book` (`bid`),
  KEY `FK_tbl_order_tbl_user` (`uid`),
  CONSTRAINT `FK_tbl_order_tbl_book` FOREIGN KEY (`bid`) REFERENCES `tbl_book` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_tbl_order_tbl_user` FOREIGN KEY (`uid`) REFERENCES `tbl_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  book.tbl_order 的数据：~1 rows (大约)
/*!40000 ALTER TABLE `tbl_order` DISABLE KEYS */;
REPLACE INTO `tbl_order` (`id`, `state`, `stime`, `etime`, `bid`, `uid`) VALUES
	(1, '已借出', '2026-03-08 22:14:06', NULL, 3, 1);
/*!40000 ALTER TABLE `tbl_order` ENABLE KEYS */;

-- 导出  表 book.tbl_user 结构
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE IF NOT EXISTS `tbl_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `user` varchar(50) NOT NULL COMMENT '真实姓名',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(50) NOT NULL COMMENT '密码',
  `mobile` varchar(50) DEFAULT NULL COMMENT '联系电话',
  `status` varchar(50) NOT NULL DEFAULT '用户' COMMENT '身份[用户,管理员]',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- 正在导出表  book.tbl_user 的数据：~3 rows (大约)
/*!40000 ALTER TABLE `tbl_user` DISABLE KEYS */;
REPLACE INTO `tbl_user` (`id`, `user`, `username`, `password`, `mobile`, `status`) VALUES
	(1, '张三', '张三', '123456', '181', '管理员'),
	(2, '李四', '李四', '123456', '182', '用户'),
	(3, '王五', '王五', '123456', '183', '用户');
/*!40000 ALTER TABLE `tbl_user` ENABLE KEYS */;

-- 导出  视图 book.tpv_order 结构
DROP VIEW IF EXISTS `tpv_order`;
-- 创建临时表以解决视图依赖性错误
CREATE TABLE `tpv_order` (
	`id` INT(11) NOT NULL COMMENT '订单id',
	`state` VARCHAR(50) NOT NULL COMMENT '状态[已借出,已售卖,已归还,超时未还]' COLLATE 'utf8mb4_general_ci',
	`stime` DATETIME NOT NULL COMMENT '借售时间',
	`etime` DATETIME NULL COMMENT '应还时间',
	`bid` INT(11) NOT NULL COMMENT '图书名',
	`uid` INT(11) NOT NULL COMMENT '关联tbl_user:借售人',
	`book` VARCHAR(50) NULL COMMENT '图书名' COLLATE 'utf8mb4_general_ci',
	`price` INT(11) NULL COMMENT '价格/元'
) ENGINE=MyISAM;

-- 导出  视图 book.v_book 结构
DROP VIEW IF EXISTS `v_book`;
-- 创建临时表以解决视图依赖性错误
CREATE TABLE `v_book` (
	`id` INT(11) NOT NULL COMMENT '图书id',
	`book` VARCHAR(50) NOT NULL COMMENT '图书名' COLLATE 'utf8mb4_general_ci',
	`price` INT(11) NOT NULL COMMENT '价格/元',
	`publisher` VARCHAR(50) NOT NULL COMMENT '出版社' COLLATE 'utf8mb4_general_ci',
	`author` VARCHAR(50) NOT NULL COMMENT '作者' COLLATE 'utf8mb4_general_ci',
	`ctime` DATETIME NOT NULL COMMENT '出版时间',
	`cid` INT(11) NULL COMMENT '关联tbl_category:图书类别',
	`category` VARCHAR(50) NULL COMMENT '图书类别' COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- 导出  视图 book.v_order 结构
DROP VIEW IF EXISTS `v_order`;
-- 创建临时表以解决视图依赖性错误
CREATE TABLE `v_order` (
	`id` INT(11) NOT NULL COMMENT '订单id',
	`state` VARCHAR(50) NOT NULL COMMENT '状态[已借出,已售卖,已归还,超时未还]' COLLATE 'utf8mb4_general_ci',
	`stime` DATETIME NOT NULL COMMENT '借售时间',
	`etime` DATETIME NULL COMMENT '应还时间',
	`bid` INT(11) NOT NULL COMMENT '图书名',
	`uid` INT(11) NOT NULL COMMENT '关联tbl_user:借售人',
	`book` VARCHAR(50) NULL COMMENT '图书名' COLLATE 'utf8mb4_general_ci',
	`price` INT(11) NULL COMMENT '价格/元',
	`user` VARCHAR(50) NULL COMMENT '真实姓名' COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- 导出  视图 book.tpv_order 结构
DROP VIEW IF EXISTS `tpv_order`;
-- 移除临时表并创建最终视图结构
DROP TABLE IF EXISTS `tpv_order`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `tpv_order` AS select `tbl_order`.`id` AS `id`,`tbl_order`.`state` AS `state`,`tbl_order`.`stime` AS `stime`,`tbl_order`.`etime` AS `etime`,`tbl_order`.`bid` AS `bid`,`tbl_order`.`uid` AS `uid`,`tbl_book`.`book` AS `book`,`tbl_book`.`price` AS `price` from (`tbl_order` left join `tbl_book` on((`tbl_order`.`bid` = `tbl_book`.`id`)));

-- 导出  视图 book.v_book 结构
DROP VIEW IF EXISTS `v_book`;
-- 移除临时表并创建最终视图结构
DROP TABLE IF EXISTS `v_book`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `v_book` AS select `tbl_book`.`id` AS `id`,`tbl_book`.`book` AS `book`,`tbl_book`.`price` AS `price`,`tbl_book`.`publisher` AS `publisher`,`tbl_book`.`author` AS `author`,`tbl_book`.`ctime` AS `ctime`,`tbl_book`.`cid` AS `cid`,`tbl_category`.`category` AS `category` from (`tbl_book` left join `tbl_category` on((`tbl_book`.`cid` = `tbl_category`.`id`)));

-- 导出  视图 book.v_order 结构
DROP VIEW IF EXISTS `v_order`;
-- 移除临时表并创建最终视图结构
DROP TABLE IF EXISTS `v_order`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `v_order` AS select `tpv_order`.`id` AS `id`,`tpv_order`.`state` AS `state`,`tpv_order`.`stime` AS `stime`,`tpv_order`.`etime` AS `etime`,`tpv_order`.`bid` AS `bid`,`tpv_order`.`uid` AS `uid`,`tpv_order`.`book` AS `book`,`tpv_order`.`price` AS `price`,`tbl_user`.`user` AS `user` from (`tpv_order` left join `tbl_user` on((`tpv_order`.`uid` = `tbl_user`.`id`)));

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
