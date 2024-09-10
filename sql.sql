/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - e-edu
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`e-edu` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `e-edu`;

/*Table structure for table `attendence` */

DROP TABLE IF EXISTS `attendence`;

CREATE TABLE `attendence` (
  `attendence_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `attendence` varchar(50) DEFAULT NULL,
  `attendence_date` date DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attendence_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `attendence` */

insert  into `attendence`(`attendence_id`,`student_id`,`attendence`,`attendence_date`,`class_id`) values (1,14,'present','2023-04-24',3),(2,10,'present','2023-04-25',10),(3,21,'present','2023-11-30',15),(4,8,'present','2023-12-07',16),(5,23,'absent','2023-12-12',17),(6,24,'present','2023-12-12',17);

/*Table structure for table `class` */

DROP TABLE IF EXISTS `class`;

CREATE TABLE `class` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `subject_alloc_id` int(11) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

/*Data for the table `class` */

insert  into `class`(`cid`,`subject_alloc_id`,`time`,`date`) values (1,1,'21:34:00','2023-04-23'),(2,7,'14:45:00','2023-04-24'),(3,8,'16:10:00','2023-04-24'),(7,8,'23:18:00','2023-04-25'),(8,8,'12:19:00','2023-04-25'),(9,8,'23:20:00','2023-04-25'),(10,6,'11:07:00','2023-04-25'),(11,6,'08:56:00','2023-04-28'),(12,1,'11:43:00','2023-04-25'),(13,11,'13:05:00','2023-04-25'),(14,12,'19:38:00','2023-11-25'),(15,12,'19:26:00','2023-11-30'),(16,5,'23:00:00','2023-12-06'),(17,13,'21:38:00','2023-12-12');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `complaint` varchar(500) DEFAULT NULL,
  `complaint_date` date DEFAULT NULL,
  `reply` varchar(500) DEFAULT NULL,
  `reply_date` date DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`student_id`,`complaint`,`complaint_date`,`reply`,`reply_date`) values (1,10,'this is a complaint','2023-04-25','this is areplay','2023-04-25'),(2,24,'vishnu sir is fast ','2023-12-12','avne nammk sheriyakkam\r\n','2023-12-12');

/*Table structure for table `course` */

DROP TABLE IF EXISTS `course`;

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(50) DEFAULT NULL,
  `dept_id` int(11) DEFAULT NULL,
  `sem` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `course` */

insert  into `course`(`course_id`,`course_name`,`dept_id`,`sem`) values (1,'BCA',1,'6'),(2,'BSC computer science',1,'6'),(3,'bsc maths',2,'6'),(4,'Bsc chemistry',3,'6'),(5,'MCA',1,'4'),(6,'economucs',4,'6'),(7,'bcom',5,'6'),(8,'mba',6,'1'),(9,'bsc.physics',7,'6');

/*Table structure for table `department` */

DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `dept_id` int(11) NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `department` */

insert  into `department`(`dept_id`,`dept_name`) values (2,'Maths'),(3,'Chemistry'),(4,'bcom'),(5,'comerse'),(6,'MCA'),(7,'PHYSICS');

/*Table structure for table `disscussion` */

DROP TABLE IF EXISTS `disscussion`;

CREATE TABLE `disscussion` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `message` varchar(500) DEFAULT NULL,
  `date` time DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `disscussion` */

insert  into `disscussion`(`chat_id`,`from_id`,`to_id`,`message`,`date`) values (1,3,2,'hi','00:00:00'),(2,2,3,'hello','00:00:00'),(3,10,4,'hi','00:00:00'),(4,13,14,'hai ','00:00:00'),(5,10,0,'hi','00:00:00'),(6,10,9,'hi','00:00:00'),(7,9,10,'hello','00:00:00'),(8,18,19,'hi','00:00:00'),(9,18,19,'hi','00:00:00'),(10,20,0,'hi','00:00:00'),(11,21,0,'hi','00:00:00'),(12,7,8,'hi','00:00:00'),(13,22,24,'ni shooperadaa','00:00:00'),(14,24,22,'hi','00:00:00');

/*Table structure for table `exam` */

DROP TABLE IF EXISTS `exam`;

CREATE TABLE `exam` (
  `exam_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(200) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `subject_alloc_id` int(11) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL,
  PRIMARY KEY (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `exam` */

insert  into `exam`(`exam_id`,`date`,`time`,`subject_alloc_id`,`marks`) values (1,'2023-04-24','14:46:00',7,20),(2,'2023-04-25','15:13:00',8,5),(3,'2023-04-24','11:15:00',6,20),(7,'2023-04-26','08:34:00',1,10),(8,'2023-04-27','09:37:00',8,10),(9,'2023-04-26','09:44:00',8,15),(10,'2023-04-26','08:57:00',6,15),(11,'2023-04-25','09:10:00',6,20),(12,'2023-04-27','09:13:00',6,20),(13,'2023-04-26','11:43:00',7,15),(14,'2023-12-08','21:55:00',5,4),(15,'2023-12-11','21:41:00',13,5);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','12345','admin'),(2,'ramyamp@gmail.com','730','staff'),(3,'abhimanyups999@gmail.com','1057','student'),(4,'priyankap@gmail.com','4295','staff'),(5,'abhinav@gmail.com','7066','student'),(6,'revathy@gmail.com','1009','staff'),(7,'ambily@gmail.com','6394','staff'),(8,'aiwin@gmail.com','2203','student'),(9,'manju@gmail.com','7795','staff'),(10,'amal@gmail.com','6915','student'),(11,'z','6744','staff'),(12,'abhijith@gmail.com','3114','student'),(13,'dannetejaimon@gmail.com','7685','staff'),(14,'abhinad@gmail.com','9398','student'),(15,'jithin2@gmail.com','3918','staff'),(16,'jhgfd@gmail.com','7108','student'),(17,'yuio@gmail.com','4766','student'),(18,'abhinavmohan453@gmail.com','2878','staff'),(19,'vishnu22@gmail.com','3689','student'),(20,'sherinregi@gmail.com','9657','staff'),(21,'nibuv_mca23-25@macfast.ac.in','6477','student'),(22,'bgfff@gmail.com','6831','staff'),(23,'gfg@gmail.com','8417','student'),(24,'j@gmail.com','9208','student');

/*Table structure for table `previous_qp` */

DROP TABLE IF EXISTS `previous_qp`;

CREATE TABLE `previous_qp` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `subid` int(11) DEFAULT NULL,
  `questpaper` varchar(1000) DEFAULT NULL,
  `year` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `previous_qp` */

insert  into `previous_qp`(`pid`,`subid`,`questpaper`,`year`) values (1,8,'/static/qp/230424150944.pdf','2022');

/*Table structure for table `question` */

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `qid` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) DEFAULT NULL,
  `question` varchar(500) DEFAULT NULL,
  `option1` varchar(100) DEFAULT NULL,
  `option2` varchar(100) DEFAULT NULL,
  `option3` varchar(100) DEFAULT NULL,
  `option4` varchar(100) DEFAULT NULL,
  `correct` varchar(100) DEFAULT NULL,
  `marks` int(10) DEFAULT NULL,
  `exam_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`qid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

/*Data for the table `question` */

insert  into `question`(`qid`,`exam_id`,`question`,`option1`,`option2`,`option3`,`option4`,`correct`,`marks`,`exam_type`) values (1,1,'Which of the following is an unsaturated hydrocarbon?','Ethane','Ethene','Ethyne','Methane','Ethene',2,'MCQ'),(2,1,'Which of the following is a saturated hydrocarbon?','Ethene','Ethyne','Ethane','Methane','Ethane',2,'MCQ'),(3,1,'Which of the following is an aromatic hydrocarbon?','Benzene','Ethene','Ethyne','Methane','Benzene',2,'MCQ'),(4,1,'write a paragraph about hydrocarbons ?','','','','','Hydrocarbons are organic chemical compounds that consist of only carbon © and hydrogen (H) atoms. Th',5,'Briefly explain'),(5,1,'explain the properties of the propane','','','','','Propane is a three-carbon alkane with the molecular formula C3H81. It is a gas at standard temperatu',9,'Briefly explain'),(8,2,'qwerty','1','2','3','4','4',5,'MCQ'),(9,3,'rrr','r','er','rrr','rr','rrr',5,'MCQ'),(10,3,'rrr','','','','','rrr',5,'Briefly explain'),(11,10,'rrr','wr','er','rrr','r','rrr',5,'MCQ'),(12,10,'47647','','','','','555',10,'Briefly explain'),(13,11,'ghgg','rr','gg','aaaaa','bb','gg',5,'MCQ'),(14,11,'rrr','','','','','eee',13,'Briefly explain'),(15,12,'eeee','','','','','hh',7,'Briefly explain'),(16,12,'squre root of 400','20','21','19','15','20',5,'MCQ'),(17,14,'qqqwer','q','w','e','r','q',4,'MCQ'),(18,15,'whos nibu?','kadhakaran','kalakaran','kadhikan','gayayakan','kadhikan',5,'MCQ');

/*Table structure for table `result` */

DROP TABLE IF EXISTS `result`;

CREATE TABLE `result` (
  `rid` int(10) NOT NULL AUTO_INCREMENT,
  `examid` int(11) DEFAULT NULL,
  `studid` int(11) DEFAULT NULL,
  `mark` int(11) DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `result` */

insert  into `result`(`rid`,`examid`,`studid`,`mark`) values (1,1,12,18),(2,3,10,10),(3,15,24,5);

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(50) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `reviews` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `review` */

insert  into `review`(`rid`,`uid`,`rating`,`reviews`,`date`) values (1,10,5,'hhh','2023-04-25');

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_name` varchar(50) DEFAULT NULL,
  `staff_gender` varchar(50) DEFAULT NULL,
  `staff_place` varchar(100) DEFAULT NULL,
  `staff_email` varchar(50) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `staff_post` varchar(100) DEFAULT NULL,
  `staff_pin` int(10) DEFAULT NULL,
  `staff_qualification` varchar(100) DEFAULT NULL,
  `dept_id` int(10) DEFAULT NULL,
  `staff_mob` bigint(10) DEFAULT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Data for the table `staff` */

insert  into `staff`(`staff_id`,`staff_name`,`staff_gender`,`staff_place`,`staff_email`,`photo`,`staff_post`,`staff_pin`,`staff_qualification`,`dept_id`,`staff_mob`) values (2,'Ramya M P','female','ichery','ramyamp@gmail.com','/static/staff_photos/230423194601.jpg','payyavoor',670633,'mtech',1,8606760852),(4,'Priyanka P','female','kannur','priyankap@gmail.com','/static/staff_photos/230423195441.jpg','kannur',670632,'MCA',1,1234567890),(6,'Revathi ganga','male','paisakary','revathy@gmail.com','/static/staff_photos/230423200748.jpg','payyavoor',670633,'B ed',1,8590428170),(7,'Ambily mathew','female','payyavoor','ambily@gmail.com','/static/staff_photos/230423201611.jpg','payyavoor',670633,'mca',1,1234567890),(9,'manju','female','sreekandapuram','manju@gmail.com','/static/staff_photos/230423202300.jpg','sreekandapuram',670631,'msc maths',2,9497556230),(11,'Angel Tom','female','thaliparamba','angletom@gmail.com','/static/staff_photos/230424133540.jpg','Thaliparamba',670633,'MSC Chemistry',3,8606760852),(13,'Danette Jaimon','female','pariyaaram','dannetejaimon@gmail.com','/static/staff_photos/230424150241.jpg','pariyaaram',670766,'bca',1,8012345678),(15,'jithin','male','thrsur','jithin2@gmail.com','/static/staff_photos/230425112738.jpg','trissurr',670985,'mca',4,4567889997),(18,'abhinav ','male','pyr','abhinavmohan453@gmail.com','/static/staff_photos/230425114959.jpg','payyavoor',670633,'bcom',5,8590428170),(20,'Sherin','male','nilamboor','sherinregi@gmail.com','/static/staff_photos/231125192949.jpg','nilamboor',970232,'bca',6,8590534271),(22,'VISHNU SIR','male','PATTIKKAD','bgfff@gmail.com','/static/staff_photos/231212212501.jpg','DEAN',434345,'MCA',7,1234056789);

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `stud_id` int(11) NOT NULL AUTO_INCREMENT,
  `stud_name` varchar(50) DEFAULT NULL,
  `stud_gender` varchar(20) DEFAULT NULL,
  `stud_place` varchar(50) DEFAULT NULL,
  `stud_post` varchar(50) DEFAULT NULL,
  `stud_pin` int(10) DEFAULT NULL,
  `stud_course_id` int(10) DEFAULT NULL,
  `stud_email` varchar(100) DEFAULT NULL,
  `semester` varchar(100) DEFAULT NULL,
  `batch` varchar(100) DEFAULT NULL,
  `stud_mob` bigint(100) DEFAULT NULL,
  `studreg` varchar(200) DEFAULT NULL,
  `photo` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`stud_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`stud_id`,`stud_name`,`stud_gender`,`stud_place`,`stud_post`,`stud_pin`,`stud_course_id`,`stud_email`,`semester`,`batch`,`stud_mob`,`studreg`,`photo`) values (3,'Abhimanyu ps','male','kelakam','Kelakam',670633,1,'abhimanyups999@gmail.com','semester1','2023-2026',8086565579,'0001','/static/student_photos/230423-194754.jpg'),(5,'Abhinav Mohan','male','payyavoor','payyavoor',670633,1,'abhinav@gmail.com','semester1','2023-2026',8086565579,'123456','/static/student_photos/230423-200113.jpg'),(8,'Awin joseph','male','ulikkal','ulikal',670632,2,'aiwin@gmail.com','semester1','2023-2026',8086565579,'0003','/static/student_photos/230423-201757.jpg'),(10,'amalnath','male','blathoor','blathoor',670631,3,'amal@gmail.com','semester1','2023-2026',8086565579,'0004','/static/student_photos/230423-202604.jpg'),(12,'Abhijith N','male','iritty','iritty',670675,4,'abhijith@gmail.com','semester1','2023',8606760862,'0005','/static/student_photos/230424-133803.jpg'),(14,'abhinad','male','payyavoor','payyavoor',670633,5,'abhinad@gmail.com','semester1','2023',8086565579,'0005','/static/student_photos/230424-150427.jpg'),(16,'ponnu','male','plustwo','ulikal',567890,6,'jhgfd@gmail.com','semester1','2023',5678987654,'678975','/static/student_photos/230425-093239.jpg'),(17,'hyuui','male','jiuytrr','tyyuuiii',567567,6,'yuio@gmail.com','semester1','3456',5678909876,'5678965','/static/student_photos/230425-093413.jpg'),(19,'vishnu','male','ckpara','ckpara',670633,7,'vishnu22@gmail.com','semester4','2023-2026',8086565579,'970633','/static/student_photos/230425-115421.jpg'),(21,'nibu','male','nilamboor','99999',999670,8,'nibuv_mca23-25@macfast.ac.in','semester1','2023-2026',8086565579,'678975','/static/student_photos/231125-193316.jpg'),(23,'nibu','male','payyavoor','kannur',233532,9,'gfg@gmail.com','semester1','2022',3214567898,'345344534','/static/student_photos/231212-212730.jpg'),(24,'nibu','male','ckdy','ulikal',123456,9,'j@gmail.com','semester1','2023',1234567898,'14434343','/static/student_photos/231212-212902.jpg');

/*Table structure for table `studymaterials` */

DROP TABLE IF EXISTS `studymaterials`;

CREATE TABLE `studymaterials` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(10) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `materials` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `studymaterials` */

insert  into `studymaterials`(`mid`,`subject_id`,`details`,`materials`) values (1,8,'module 1','/static/notes/230424-150904.pdf'),(2,11,'module 1','/static/notes/230425-120344.pdf'),(3,14,'vvv','/static/notes/231212-213440.pdf');

/*Table structure for table `suballocatecourse` */

DROP TABLE IF EXISTS `suballocatecourse`;

CREATE TABLE `suballocatecourse` (
  `suballoc_courseid` int(10) NOT NULL AUTO_INCREMENT,
  `course_id` int(10) DEFAULT NULL,
  `subject_id` int(10) DEFAULT NULL,
  `sems` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`suballoc_courseid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `suballocatecourse` */

insert  into `suballocatecourse`(`suballoc_courseid`,`course_id`,`subject_id`,`sems`) values (1,1,1,'semester1'),(3,1,2,'semester1'),(4,1,3,'semester1'),(5,2,4,'semester1'),(6,3,5,'semester1'),(7,4,6,'semester1'),(8,5,7,'semester1'),(9,6,8,'semester1'),(10,2,1,'semester1'),(11,7,9,'semester4'),(12,8,10,'semester1'),(13,1,2,'semester5'),(14,9,11,'semester1');

/*Table structure for table `subject` */

DROP TABLE IF EXISTS `subject`;

CREATE TABLE `subject` (
  `sub_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_name` varchar(50) DEFAULT NULL,
  `syllabus` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `subject` */

insert  into `subject`(`sub_id`,`sub_name`,`syllabus`) values (1,'informatics','/static/syllabus/230423-194851.pdf'),(2,'c programming','/static/syllabus/230423-195329.pdf'),(3,'English Complementary for BCA 1','/static/syllabus/230423-200837.pdf'),(4,'Statictics','/static/syllabus/230423-201853.pdf'),(5,'mathematics for bsc maths 1','/static/syllabus/230423-202649.pdf'),(6,'hydro carbons','/static/syllabus/230424-133901.pdf'),(7,'Statitics','/static/syllabus/230424-150534.pdf'),(8,'computer','/static/syllabus/230425-093519.pdf'),(9,'accountency','/static/syllabus/230425-115734.pdf'),(10,'webproject','/static/syllabus/231125-193445.pdf'),(11,'mechanics','/static/syllabus/231212-212958.pdf');

/*Table structure for table `subject_alloc` */

DROP TABLE IF EXISTS `subject_alloc`;

CREATE TABLE `subject_alloc` (
  `suballoc_courseid` int(11) NOT NULL AUTO_INCREMENT,
  `suballoccourseid` int(11) DEFAULT NULL,
  `staff_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`suballoc_courseid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `subject_alloc` */

insert  into `subject_alloc`(`suballoc_courseid`,`suballoccourseid`,`staff_id`) values (1,1,2),(2,2,4),(3,3,4),(4,4,6),(5,5,7),(6,6,9),(7,7,11),(8,8,13),(9,9,15),(10,10,4),(11,11,18),(12,12,20),(13,14,22);

/*Table structure for table `suggestions` */

DROP TABLE IF EXISTS `suggestions`;

CREATE TABLE `suggestions` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) DEFAULT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `suggestions` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
