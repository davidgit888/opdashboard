-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- Server version:               8.0.15 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL 版本:                  10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping data for table smallpart.smallparts_group: ~4 rows (approximately)
/*!40000 ALTER TABLE `smallparts_group` DISABLE KEYS */;
INSERT INTO `smallparts_group` (`id`, `group_name`) VALUES
	(6, 'Global A X'),
	(7, 'Global A Y'),
	(8, 'Global A Z'),
	(9, '驱动轮粘接');
/*!40000 ALTER TABLE `smallparts_group` ENABLE KEYS */;

-- Dumping data for table smallpart.smallparts_partlist: ~25 rows (approximately)
/*!40000 ALTER TABLE `smallparts_partlist` DISABLE KEYS */;
INSERT INTO `smallparts_partlist` (`id`, `name`, `group_id`) VALUES
	(1, '162-2139', 6),
	(2, 'B545-0201-1-2', 6),
	(3, 'H00005736', 6),
	(4, 'H00005735', 6),
	(5, '162-2140', 7),
	(6, 'B545-0701-3-2', 7),
	(7, 'H00005618', 7),
	(8, 'H00005617', 7),
	(9, '162-2141', 8),
	(10, 'B545-0101-2', 8),
	(11, 'H00006253', 8),
	(12, 'H003928', 9),
	(13, '162-401-100-1-3', 9),
	(14, '162-4-1-102-4', 9),
	(15, 'G17091000', 9),
	(16, 'G17091100', 9),
	(17, 'G17049202', 9),
	(18, 'G17049502', 9),
	(19, 'G17049800', 9),
	(20, 'G17091200', 9),
	(21, 'G17091300', 9),
	(22, 'B545-0103-1', 9),
	(23, 'B545-2111-1', 9),
	(24, 'B616-0201-1', 9),
	(25, 'B616-0202-1', 9);
/*!40000 ALTER TABLE `smallparts_partlist` ENABLE KEYS */;

-- Dumping data for table smallpart.smallparts_sfmajd: ~44 rows (approximately)
/*!40000 ALTER TABLE `smallparts_sfmajd` DISABLE KEYS */;
INSERT INTO `smallparts_sfmajd` (`id`, `shift`, `adj_date`, `adj_reason`, `adj_nbr`) VALUES
	(49, 'lufeng', '2019-05-13', '缺件', 1),
	(50, 'lufeng', '2019-05-13', '排产不饱满', 2),
	(51, 'lufeng', '2019-05-13', '花岗石未进厂', 3),
	(52, 'lufeng', '2019-05-13', '其他', 2),
	(58, 'lufeng', '2019-05-11', '排产不饱满', 2),
	(59, 'lufeng', '2019-05-11', '花岗石未进厂', 1),
	(60, 'lufeng', '2019-05-10', '缺件', 2),
	(63, 'lufeng', '2019-05-10', '其他', 1),
	(64, 'lufeng', '2019-05-09', '缺件', 2),
	(66, 'lufeng', '2019-05-09', '花岗石未进厂', 2),
	(69, 'lufeng', '2019-05-08', '花岗石未进厂', 1),
	(70, 'lufeng', '2019-05-13', '排产不饱满', 1),
	(71, 'lufeng', '2019-05-13', '花岗石未进厂', 2),
	(72, 'lufeng', '2019-05-13', '花岗石未进厂', 2),
	(73, 'lufeng', '2019-05-13', '其他', 3),
	(74, 'lufeng', '2019-05-07', '花岗石未进厂', 1),
	(75, 'lufeng', '2019-05-07', '其他', 2),
	(76, 'lufeng', '2019-05-06', '缺件', 2),
	(77, 'lufeng', '2019-05-06', '花岗石未进厂', 1),
	(78, 'wangshuai', '2019-05-13', '缺件', 1),
	(79, 'wangshuai', '2019-05-13', '排产不饱满', 2),
	(82, 'wangshuai', '2019-05-11', '缺件', 3),
	(83, 'wangshuai', '2019-05-11', '排产不饱满', 2),
	(84, 'wangshuai', '2019-05-10', '缺件', 1),
	(85, 'wangshuai', '2019-05-10', '排产不饱满', 1),
	(86, 'wangshuai', '2019-05-10', '花岗石未进厂', 2),
	(87, 'wangshuai', '2019-05-09', '排产不饱满', 3),
	(88, 'wangshuai', '2019-05-09', '花岗石未进厂', 2),
	(89, 'wangshuai', '2019-05-07', '缺件', 3),
	(90, 'wangshuai', '2019-05-07', '排产不饱满', 2),
	(91, 'wangshuai', '2019-05-07', '花岗石未进厂', 3),
	(92, 'wangshuai', '2019-05-07', '其他', 1),
	(93, 'lufeng', '2019-05-13', '缺件', 3),
	(94, 'lufeng', '2019-05-13', '花岗石未进厂', 1),
	(95, 'lufeng', '2019-05-11', '缺件', 1),
	(96, 'lufeng', '2019-05-11', '排产不饱满', 1),
	(97, 'lufeng', '2019-05-11', '花岗石未进厂', 1),
	(98, 'lufeng', '2019-05-11', '其他', 1),
	(99, 'lufeng', '2019-05-14', '缺件', 2),
	(100, 'lufeng', '2019-05-14', '排产不饱满', 1),
	(101, 'lufeng', '2019-05-14', '缺件', 2),
	(102, 'lufeng', '2019-05-14', '排产不饱满', 3),
	(103, 'lufeng', '2019-05-14', '缺件', 3),
	(104, 'lufeng', '2019-05-14', '花岗石未进厂', 1);
/*!40000 ALTER TABLE `smallparts_sfmajd` ENABLE KEYS */;

-- Dumping data for table smallpart.smallparts_sheetconfig: ~5 rows (approximately)
/*!40000 ALTER TABLE `smallparts_sheetconfig` DISABLE KEYS */;
INSERT INTO `smallparts_sheetconfig` (`id`, `title`, `config_string`, `is_active`, `comments`, `group_id`, `version`) VALUES
	(7, 'Global A X向减速器装配工序记录表', '$10|拾取装配用零件|检查零件外观\r\n$10.1|拾取装配用零件|清理，将装配零件的表面清理干净\r\n$20.1|驱动轮组件装配|在有相对运动的部位涂适量润滑脂\r\n$20.2|驱动轮组件装配|按照装配工艺进行装配\r\n$30.1|安装从动轮|按照装配工艺安装从动轮\r\n$30.2|安装从动轮|在涨紧套落定上涂LOCTITE243胶，然后用4±0.25N-m的扭矩上紧\r\n$40|驱动轮组件与X点击支架结合|将驱动轮组件安装在点击支架的安装孔中，调整驱动轮组件的固定孔，然后用M5X25的落定将其锁紧并检查是否有干涉\r\n$50.1|安装电机部件|将电机与连接法兰用落定连接\r\n$50.2|安装电机部件|将电机部件安装在X向电机支架上\r\n$60.1|安装传动带|用直尺找正主动轮与从动轮的准直\r\n$60.2|安装传动带|将传动带安装在主动轮与从动轮上\r\n$60.3|安装传动带|调整传动带的张紧力至263-274Hz|num', 1, '初次创建', 6, 1),
	(8, 'Global A Y向减速器装配工序记录表', '$10|拾取装配用零件|检查零件外观\r\n$10.1|拾取装配用零件|清理，将装配零件的表面清理干净\r\n$20.1|驱动轮组件装配|在有相对运动的部位涂适量润滑脂\r\n$20.2|驱动轮组件装配|按照装配工艺进行装配\r\n$30.1|安装从动轮|按照装配工艺安装从动轮\r\n$30.2|安装从动轮|在涨紧套落定上涂LOCTITE243胶，然后用4±0.25N-m的扭矩上紧\r\n$40|驱动轮组件与X点击支架结合|将驱动轮组件安装在点击支架的安装孔中，调整驱动轮组件的固定孔，然后用M5X16的落定将其锁紧并检查是否有干涉\r\n$50.1|安装电机部件|将电机与连接法兰用螺钉连接\r\n$50.2|安装电机部件|将电机部件安装在X向电机支架上\r\n$60.1|安装传动带|用直尺赵正主动轮与从动轮的准直\r\n$60.2|安装传动带|将传动带安装在主动轮与从动轮上\r\n$60.3|安装传动带|调整传动带的张紧力至263-274Hz|num', 1, '初次创建', 7, 1),
	(9, 'Global A Z向减速器装配工序记录表', '$10|拾取装配用零件|检查零件外观\r\n$10.1|拾取装配用零件|清理，将装配零件的表面清理干净\r\n$20.1|驱动轮组件装配|在有相对运动的部位涂适量润滑脂\r\n$20.2|驱动轮组件装配|按照装配工艺进行装配\r\n$30.1|安装从动轮|按照装配工艺安装从动轮\r\n$30.2|安装从动轮|在涨紧套落定上涂LOCTITE243胶，然后用4±0.25N-m的扭矩上紧\r\n$40|部件测试|用手转动从动轮检查是否有运动干涉与额外噪音', 1, '初次创建\r\nV1版本问题：$40忘记填写工序内容', 8, 1),
	(10, '电机驱动轮粘接工序记录表', '$10|清洗|将驱动轮的内孔及电机轴的粘接面用酒精清洗，直到其粘接面干净为止。\r\n$20|涂施LOCTITE648|经LOCTITE648胶呈珠状均匀涂抹在电机的主轴上；同样将LOCTITE648胶呈珠状均匀涂抹在驱动轮的孔壁上（包括轴肩部分）。\r\n$30|粘接|将驱动轮套在电机的主轴上，沿螺旋线状推进驱动轮，直到驱动轮的轴向距离符合图纸为止\r\n$40|清理|将多余的胶擦拭干净（包括电机轴和驱动轮）。\r\n$50|固化|将粘接好的电机组件呈水平放置，最少停放24小时。\r\n$50.1|固化|固化开始时间。|date\r\n$50.2|固化|固化结束时间。|date\r\n$60.1|检验|检查粘接位置是否符合图纸要求。\r\n$60.2|检验|按照装配工艺进行扭矩测试，保证其粘接扭矩不小于100IN/LBS(11.3N-m),抽样比率1:5。\r\n$60.3|检验|胶固化后，旋转电机轴，检查电机轴转动是否异常。\r\n$70|记录电机编号|记录电机序列号，零件号。|str', 1, '初次创建', 9, 1),
	(11, '电机驱动轮粘接工序记录表', '$10|清洗|将驱动轮的内孔及电机轴的粘接面用酒精清洗，直到其粘接面干净为止。\r\n$20|涂施LOCTITE_648|经LOCTITE_648胶呈珠状均匀涂抹在电机的主轴上；同样将LOCTITE_648胶呈珠状均匀涂抹在驱动轮的孔壁上（包括轴肩部分）。\r\n$30|粘接|将驱动轮套在电机的主轴上，沿螺旋线状推进驱动轮，直到驱动轮的轴向距离符合图纸为止\r\n$40|清理|将多余的胶擦拭干净（包括电机轴和驱动轮）。\r\n$50|固化|将粘接好的电机组件呈水平放置，最少停放24小时。\r\n$50.1|固化|固化开始时间。|date\r\n$50.2|固化|固化结束时间。|date|canbeopen\r\n$60.1|检验|检查粘接位置是否符合图纸要求。|canbeopen\r\n$60.2|检验|按照装配工艺进行扭矩测试，保证其粘接扭矩不小于100IN/LBS(11.3N-m),抽样比率1:5。|notall|canbeopen\r\n$60.3|检验|胶固化后，旋转电机轴，检查电机轴转动是否异常。|canbeopen\r\n$70|记录电机编号|记录电机序列号，零件号。|str|sntaken', 1, '新版本测试，将LOCTITE648修改成LOCTITE_648', 9, 2);
/*!40000 ALTER TABLE `smallparts_sheetconfig` ENABLE KEYS */;

-- Dumping data for table smallpart.smallparts_specification: ~29 rows (approximately)
/*!40000 ALTER TABLE `smallparts_specification` DISABLE KEYS */;
INSERT INTO `smallparts_specification` (`id`, `part`, `machine`) VALUES
	(1, 'H00006253', 'Global S A Green/Blue/Chrome'),
	(2, 'B545-0101-2', 'Inspector/Explorer/Pioneer(+)/Global Plus 5,6,8系列'),
	(3, '162-2141', 'Global A'),
	(4, '162-2140', 'Global A'),
	(5, 'B545-0701-3-2', 'Inspector/Explorer/Pioneer(+)/Global Plus 5,6,8系列'),
	(6, 'H00005618', 'Global S A Green'),
	(7, 'H00005617', 'Global S A Blue/Chrome'),
	(8, '162-2139', 'Global A'),
	(9, 'B545-0201-1-2', 'Inspector/Explorer/Pioneer(+)/Global Plus 5,6,8系列'),
	(10, 'H00005736', 'Global S A Green'),
	(11, 'H00005735', 'Global S A Blue/Chrome'),
	(12, 'H003928', 'null'),
	(13, '162-401-100-1-3', 'null'),
	(14, '162-401-102-4', 'null'),
	(15, 'G17091000', 'null'),
	(16, 'G17091100', 'null'),
	(17, 'G17049202', 'null'),
	(18, 'G17049502', 'null'),
	(19, 'G17090800', 'null'),
	(20, 'G17090900', 'null'),
	(21, 'G1749900', 'null'),
	(22, 'G17091500', 'null'),
	(23, 'G17049800', 'null'),
	(24, 'G1791200', 'null'),
	(25, 'G17091300', 'null'),
	(26, 'B545-0103-1', 'null'),
	(27, 'B545-2111-1', 'null'),
	(28, 'B616-0201-1', 'null'),
	(29, 'B616-0202-1', 'null');
/*!40000 ALTER TABLE `smallparts_specification` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
