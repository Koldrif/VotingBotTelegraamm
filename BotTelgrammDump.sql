CREATE DATABASE  IF NOT EXISTS `5SbqamHdMU` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_ru_0900_as_cs */;
USE `5SbqamHdMU`;
-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: remotemysql.com    Database: 5SbqamHdMU
-- ------------------------------------------------------
-- Server version	8.0.13-4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dictionary_of_pairs`
--

DROP TABLE IF EXISTS `dictionary_of_pairs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `dictionary_of_pairs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_expr` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `second_expr` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dictionary_of_pairs`
--

LOCK TABLES `dictionary_of_pairs` WRITE;
/*!40000 ALTER TABLE `dictionary_of_pairs` DISABLE KEYS */;
INSERT INTO `dictionary_of_pairs` VALUES (1,'большой деревянный дом','деревянный большой дом'),(2,'маленький синий дом','синий маленький дом'),(3,'высокий красный забор ','красный высокий забор'),(4,'низкий металлический забор','металлический низкий забор'),(5,'джинсовая длинная рубашка','длинная джинсовая рубашка'),(6,'джинсовая серая рубашка','серая джинсовая рубашка'),(7,'раннее зимнее утро','зимнее раннее утро'),(8,'летний золотистый вечер','золотистый летний вечер'),(9,'узкая кирпичная дорожка','кирпичная узкая дорожка'),(10,'широкое быстрое шоссе','быстрое широкое шоссе'),(11,'розовое короткое платье','короткое розовое платье'),(12,'красивое короткое платье','короткое красивое платье'),(13,'сильные мускулистые руки','мускулистые сильные руки'),(14,'слабые тонкие пальцы','тонкие слабые пальцы'),(15,'глубокие голубые глаза','голубые глубокие глаза'),(16,'большие красивые глаза','красивые большие глаза'),(17,'высокое стеклянное здание','стеклянное высокое здание'),(18,'маленький стеклянный шар','стеклянный маленький шар'),(19,'красивый зелёный пейзаж','зелёный красивый пейзаж'),(20,'причудливое зелёное дерево','зелёное причудливое дерево'),(21,'странная цветная одежда','цветная странная одежда'),(22,'странное цветное платье','цветное странное платье'),(23,'большие серебрянные ложки','серебрянные большие ложки'),(24,'большие серебрянные серёжки','серебрянные большие серёжки'),(25,'густая седая борода','седая густая борода'),(26,'длинные жидкие волосы','жидкие длинные волосы'),(27,'высокий красивый парень','красивый высокий парень'),(28,'милая миниатюрная девушка','миниатюрная милая девушка'),(29,'старый добрый пёс','добрый старый пёс'),(30,'молодой быстрый жеребец','быстрый молодой жеребец'),(31,'старый вредный учитель','вредный старый учитель'),(32,'молодой добрый врач','добрый молодой врач'),(33,'умный прилежный ученик','прилежный умный ученик'),(34,'отстающий ленивый ученик','ленивый отстающий ученик'),(35,'известный виртуозный музыкант','виртуозный извечтный музыкант'),(36,'начинающий талантливый режиссёр','талантливый начинающий режиссёр'),(37,'юный бесстрашный альпенист','бесстрашный юный альпенист'),(38,'молодой смелый гонщик','смелый молодой гонщик'),(39,'плаксивый маленький ребенок','маленький плаксивый ребенок'),(40,'обидчивый вредный мальчик','вредный обидчивый мальчик'),(41,'серая маленькая мышь','маленькая серая мышь'),(42,'рыжая быстрая лошадь','быстрая рыжая лошадь'),(43,'полосатый ласковый кот','ласковый полосатый кот'),(44,'пернистый разноцветный попугай','разноцветный пернистый попугай'),(45,'кудрявая белая овечка','белая кудрявая овечка'),(46,'кучерявый чёрный баран','чёрный кучерявый баран'),(47,'маленькая сообразительная девочка','сообразительная маленькая девочка'),(48,'взрослый бестолковый человек','бестолковый взрослый человек'),(49,'ленивый полосатый кот','полосатый ленивый кот'),(50,'ловкая пушистая белка','пушистая ловкая белка');
/*!40000 ALTER TABLE `dictionary_of_pairs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link_table`
--

DROP TABLE IF EXISTS `link_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `link_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_dictionary` int(11) NOT NULL,
  `firs_expr_amount_of_votes` int(11) NOT NULL,
  `second_expr_amount_of_votes` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `link_table_fk0` (`id_dictionary`),
  CONSTRAINT `link_table_fk0` FOREIGN KEY (`id_dictionary`) REFERENCES `dictionary_of_pairs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link_table`
--

LOCK TABLES `link_table` WRITE;
/*!40000 ALTER TABLE `link_table` DISABLE KEYS */;
INSERT INTO `link_table` VALUES (1,1,13,7),(2,2,12,7),(3,3,19,8),(4,4,15,8),(5,5,18,13),(6,6,11,8),(7,7,18,11),(8,8,18,11),(9,9,9,11),(10,10,13,9),(11,11,11,9),(12,12,14,12),(13,13,13,9),(14,14,13,9),(15,15,13,15),(16,16,12,5),(17,17,10,9),(18,18,16,6),(19,19,17,6),(20,20,12,9),(21,21,13,10),(22,22,14,10),(23,23,14,7),(24,24,17,8),(25,25,12,10),(26,26,19,8),(27,27,13,14),(28,28,10,8),(29,29,16,12),(30,30,11,7),(31,31,17,5),(32,32,18,11),(33,33,14,7),(34,34,16,8),(35,35,11,13),(36,36,8,12),(37,37,11,10),(38,38,11,13),(39,39,15,12),(40,40,13,8),(41,41,17,16),(42,42,15,13),(43,43,15,5),(44,44,11,14),(45,45,13,11),(46,46,17,10),(47,47,15,8),(48,48,17,8),(49,49,18,9),(50,50,12,8);
/*!40000 ALTER TABLE `link_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-21 22:38:33
