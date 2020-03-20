-- MySQL dump 10.13  Distrib 5.7.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: statistic_db
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.19-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `toutiao_tb`
--

DROP TABLE IF EXISTS `toutiao_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toutiao_tb` (
  `total_data` bigint(20) unsigned DEFAULT '0' COMMENT '数据总量',
  `cycle_type` varchar(3) DEFAULT '1' COMMENT '周期类型',
  `cycle_num` int(11) DEFAULT '0' COMMENT '周期量',
  `account_total` int(10) unsigned DEFAULT '0' COMMENT '用户总量条数',
  `account_cycle_num` int(11) DEFAULT '0' COMMENT '用户周期数量',
  `article_total` bigint(20) unsigned DEFAULT '0' COMMENT '文章总量',
  `article_cycle_num` int(11) DEFAULT '0' COMMENT '文章周期量',
  `article_text_total` int(11) DEFAULT '0',
  `article_text_cycle_num` int(11) DEFAULT '0',
  `article_micro_total` int(11) DEFAULT '0',
  `article_micro_cycle_num` int(11) DEFAULT '0',
  `article_video_total` int(11) DEFAULT '0',
  `article_video_cycle_num` int(11) DEFAULT '0',
  `update_total` int(11) DEFAULT '0',
  `update_cycle_num` int(11) DEFAULT '0',
  `updata_micro_total` int(11) DEFAULT '0',
  `update_micro_cycle` int(11) DEFAULT '0',
  `update_text_total` int(11) DEFAULT '0',
  `update_text_cycle` int(11) DEFAULT '0',
  `update_video_total` int(11) DEFAULT '0',
  `update_video_cycle` int(11) DEFAULT '0',
  `comment_total` bigint(20) unsigned DEFAULT '0',
  `comment_cycle` int(11) DEFAULT '0',
  `video_total` bigint(20) unsigned DEFAULT '0',
  `video_cycle` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='头条数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `toutiao_tb`
--

LOCK TABLES `toutiao_tb` WRITE;
/*!40000 ALTER TABLE `toutiao_tb` DISABLE KEYS */;
/*!40000 ALTER TABLE `toutiao_tb` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-13 11:37:29
