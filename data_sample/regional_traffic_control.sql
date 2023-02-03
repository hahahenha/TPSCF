/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50624
 Source Host           : localhost:3306
 Source Schema         : regional_traffic_control

 Target Server Type    : MySQL
 Target Server Version : 50624
 File Encoding         : 65001

 Date: 23/09/2022 21:02:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for phases_detail
-- ----------------------------
DROP TABLE IF EXISTS `phases_detail`;
CREATE TABLE `phases_detail`  (
  `INTERSECTION_ID` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `PHASE_NUM` int(11) NOT NULL,
  `PHASE_DETAIL` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `MIN_GREEN_TIME` int(11) NULL DEFAULT NULL,
  `MAX_GREEN_TIME` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`INTERSECTION_ID`, `PHASE_NUM`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of phases_detail
-- ----------------------------
INSERT INTO `phases_detail` VALUES ('HS001', 1, '000001111000001111', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 2, '000002221000002221', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 3, '000000001000000001', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 4, '000000002000000002', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 5, '111110000111110000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 6, '222210000222210000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 7, '000010000000010000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS001', 8, '000020000000020000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 1, '000001111000001111', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 2, '000002221000002221', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 3, '000000001000000001', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 4, '000000002000000002', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 5, '111110000111110000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 6, '222210000222210000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 7, '000010000000010000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS002', 8, '000020000000020000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 1, '000111000111', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 2, '000221000221', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 3, '000001000001', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 4, '000002000002', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 5, '111000111000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 6, '221000221000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 7, '001000001000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS003', 8, '002000002000', 14, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 1, '00111111', 12, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 2, '00222221', 12, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 3, '00000001', 12, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 4, '00000002', 12, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 5, '11100000', 12, 120);
INSERT INTO `phases_detail` VALUES ('HS004', 6, '22200000', 12, 120);
INSERT INTO `phases_detail` VALUES ('NS001', 0, '11111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS002', 0, '11111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS003', 0, '11111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS004', 0, '111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS005', 0, '1111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS006', 0, '1111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS007', 0, '11111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS008', 0, '11111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS009', 0, '1111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS010', 0, '1111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS011', 0, '111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS012', 0, '11111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS013', 0, '1111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS014', 0, '111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS015', 0, '11111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS016', 0, '111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS017', 0, '111111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS018', 0, '11111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS019', 0, '111111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS020', 0, '111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS021', 0, '1111111111111111', 0, 255);
INSERT INTO `phases_detail` VALUES ('NS022', 0, '111111', 0, 255);

-- ----------------------------
-- Table structure for road_lanes
-- ----------------------------
DROP TABLE IF EXISTS `road_lanes`;
CREATE TABLE `road_lanes`  (
  `ROAD_ID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `LANE_NUM` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ROAD_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of road_lanes
-- ----------------------------
INSERT INTO `road_lanes` VALUES ('HS001#0#01', 3);
INSERT INTO `road_lanes` VALUES ('HS001#0#02', 2);
INSERT INTO `road_lanes` VALUES ('HS001#0#03', 3);
INSERT INTO `road_lanes` VALUES ('HS001#0#04', 2);
INSERT INTO `road_lanes` VALUES ('HS001#1#01', 3);
INSERT INTO `road_lanes` VALUES ('HS001#1#02', 2);
INSERT INTO `road_lanes` VALUES ('HS001#1#04', 2);
INSERT INTO `road_lanes` VALUES ('HS002#0#01', 3);
INSERT INTO `road_lanes` VALUES ('HS002#0#02', 2);
INSERT INTO `road_lanes` VALUES ('HS002#0#03', 3);
INSERT INTO `road_lanes` VALUES ('HS002#0#04', 2);
INSERT INTO `road_lanes` VALUES ('HS002#1#03', 3);
INSERT INTO `road_lanes` VALUES ('HS002#1#04', 2);
INSERT INTO `road_lanes` VALUES ('HS003#0#01', 1);
INSERT INTO `road_lanes` VALUES ('HS003#0#02', 1);
INSERT INTO `road_lanes` VALUES ('HS003#0#03', 1);
INSERT INTO `road_lanes` VALUES ('HS003#0#04', 1);
INSERT INTO `road_lanes` VALUES ('HS003#1#04', 1);
INSERT INTO `road_lanes` VALUES ('HS004#0#01', 2);
INSERT INTO `road_lanes` VALUES ('HS004#0#02', 1);
INSERT INTO `road_lanes` VALUES ('HS004#0#03', 2);
INSERT INTO `road_lanes` VALUES ('HS004#1#03', 2);
INSERT INTO `road_lanes` VALUES ('NS001#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS001#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS001#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS001#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS001#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS001#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS002#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS002#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS002#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS002#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS002#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS002#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS003#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS003#0#02', 2);
INSERT INTO `road_lanes` VALUES ('NS003#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS003#1#01', 2);
INSERT INTO `road_lanes` VALUES ('NS003#1#02', 2);
INSERT INTO `road_lanes` VALUES ('NS004#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS004#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS004#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS004#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS004#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS004#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS005#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS005#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS005#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS005#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS005#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS006#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS006#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS006#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS006#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS006#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS007#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS007#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS007#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS007#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS007#1#03', 2);
INSERT INTO `road_lanes` VALUES ('NS008#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS008#0#02', 2);
INSERT INTO `road_lanes` VALUES ('NS008#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS008#1#02', 2);
INSERT INTO `road_lanes` VALUES ('NS009#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS009#0#02', 2);
INSERT INTO `road_lanes` VALUES ('NS009#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS009#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS009#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS010#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS010#0#02', 2);
INSERT INTO `road_lanes` VALUES ('NS010#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS010#1#01', 2);
INSERT INTO `road_lanes` VALUES ('NS010#1#02', 2);
INSERT INTO `road_lanes` VALUES ('NS010#1#03', 2);
INSERT INTO `road_lanes` VALUES ('NS011#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS011#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS011#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS011#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS012#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS012#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS012#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS012#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS012#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS013#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS013#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS013#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS013#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS013#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS014#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS014#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS014#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS014#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS014#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS015#0#01', 3);
INSERT INTO `road_lanes` VALUES ('NS015#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS015#0#03', 3);
INSERT INTO `road_lanes` VALUES ('NS016#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS016#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS016#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS016#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS017#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS017#0#02', 2);
INSERT INTO `road_lanes` VALUES ('NS017#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS018#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS018#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS018#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS018#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS018#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS018#1#03', 1);
INSERT INTO `road_lanes` VALUES ('NS019#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS019#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS019#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS019#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS020#0#01', 2);
INSERT INTO `road_lanes` VALUES ('NS020#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS020#0#03', 2);
INSERT INTO `road_lanes` VALUES ('NS020#1#01', 2);
INSERT INTO `road_lanes` VALUES ('NS020#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS021#0#01', 3);
INSERT INTO `road_lanes` VALUES ('NS021#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS021#0#03', 3);
INSERT INTO `road_lanes` VALUES ('NS021#0#04', 1);
INSERT INTO `road_lanes` VALUES ('NS021#1#01', 3);
INSERT INTO `road_lanes` VALUES ('NS021#1#02', 1);
INSERT INTO `road_lanes` VALUES ('NS021#1#03', 3);
INSERT INTO `road_lanes` VALUES ('NS021#1#04', 1);
INSERT INTO `road_lanes` VALUES ('NS022#0#01', 1);
INSERT INTO `road_lanes` VALUES ('NS022#0#02', 1);
INSERT INTO `road_lanes` VALUES ('NS022#0#03', 1);
INSERT INTO `road_lanes` VALUES ('NS022#1#01', 1);
INSERT INTO `road_lanes` VALUES ('NS022#1#02', 1);

-- ----------------------------
-- Table structure for road_relation
-- ----------------------------
DROP TABLE IF EXISTS `road_relation`;
CREATE TABLE `road_relation`  (
  `ROAD_ID_FROM` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FROM_LANE_ID` int(11) NOT NULL,
  `ROAD_ID_TO` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DIRECTION` int(11) NULL DEFAULT NULL,
  `INTERSECTION_ID` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `CONTROL_ORDER` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ROAD_ID_FROM`, `FROM_LANE_ID`, `ROAD_ID_TO`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of road_relation
-- ----------------------------
INSERT INTO `road_relation` VALUES ('HS001#0#01', 0, 'HS001#1#04', 7, 'HS001', 10);
INSERT INTO `road_relation` VALUES ('HS001#0#01', 0, 'NS015#0#01', 3, 'HS001', 11);
INSERT INTO `road_relation` VALUES ('HS001#0#01', 1, 'NS015#0#01', 3, 'HS001', 12);
INSERT INTO `road_relation` VALUES ('HS001#0#01', 2, 'HS001#1#02', 2, 'HS001', 14);
INSERT INTO `road_relation` VALUES ('HS001#0#01', 2, 'NS015#0#01', 3, 'HS001', 13);
INSERT INTO `road_relation` VALUES ('HS001#0#02', 0, 'HS001#1#01', 7, 'HS001', 15);
INSERT INTO `road_relation` VALUES ('HS001#0#02', 0, 'HS001#1#04', 3, 'HS001', 16);
INSERT INTO `road_relation` VALUES ('HS001#0#02', 1, 'HS001#1#04', 3, 'HS001', 17);
INSERT INTO `road_relation` VALUES ('HS001#0#02', 1, 'NS015#0#01', 2, 'HS001', 18);
INSERT INTO `road_relation` VALUES ('HS001#0#03', 0, 'HS001#1#01', 3, 'HS001', 2);
INSERT INTO `road_relation` VALUES ('HS001#0#03', 0, 'HS001#1#02', 7, 'HS001', 1);
INSERT INTO `road_relation` VALUES ('HS001#0#03', 1, 'HS001#1#01', 3, 'HS001', 3);
INSERT INTO `road_relation` VALUES ('HS001#0#03', 2, 'HS001#1#01', 3, 'HS001', 4);
INSERT INTO `road_relation` VALUES ('HS001#0#03', 2, 'HS001#1#04', 2, 'HS001', 5);
INSERT INTO `road_relation` VALUES ('HS001#0#04', 0, 'HS001#1#02', 3, 'HS001', 7);
INSERT INTO `road_relation` VALUES ('HS001#0#04', 0, 'NS015#0#01', 7, 'HS001', 6);
INSERT INTO `road_relation` VALUES ('HS001#0#04', 1, 'HS001#1#01', 2, 'HS001', 9);
INSERT INTO `road_relation` VALUES ('HS001#0#04', 1, 'HS001#1#02', 3, 'HS001', 8);
INSERT INTO `road_relation` VALUES ('HS001#1#02', -1, 'NS002#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('HS001#1#04', -1, 'NS003#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('HS002#0#01', 0, 'HS002#1#03', 3, 'HS002', 11);
INSERT INTO `road_relation` VALUES ('HS002#0#01', 0, 'HS002#1#04', 7, 'HS002', 10);
INSERT INTO `road_relation` VALUES ('HS002#0#01', 1, 'HS002#1#03', 3, 'HS002', 12);
INSERT INTO `road_relation` VALUES ('HS002#0#01', 2, 'HS002#1#03', 3, 'HS002', 13);
INSERT INTO `road_relation` VALUES ('HS002#0#01', 2, 'NS016#0#03', 2, 'HS002', 14);
INSERT INTO `road_relation` VALUES ('HS002#0#02', 0, 'HS002#1#04', 3, 'HS002', 16);
INSERT INTO `road_relation` VALUES ('HS002#0#02', 0, 'NS015#0#03', 7, 'HS002', 15);
INSERT INTO `road_relation` VALUES ('HS002#0#02', 1, 'HS002#1#03', 2, 'HS002', 18);
INSERT INTO `road_relation` VALUES ('HS002#0#02', 1, 'HS002#1#04', 3, 'HS002', 17);
INSERT INTO `road_relation` VALUES ('HS002#0#03', 0, 'NS015#0#03', 3, 'HS002', 2);
INSERT INTO `road_relation` VALUES ('HS002#0#03', 0, 'NS016#0#03', 7, 'HS002', 1);
INSERT INTO `road_relation` VALUES ('HS002#0#03', 1, 'NS015#0#03', 3, 'HS002', 3);
INSERT INTO `road_relation` VALUES ('HS002#0#03', 2, 'HS002#1#04', 2, 'HS002', 5);
INSERT INTO `road_relation` VALUES ('HS002#0#03', 2, 'NS015#0#03', 3, 'HS002', 4);
INSERT INTO `road_relation` VALUES ('HS002#0#04', 0, 'HS002#1#03', 7, 'HS002', 6);
INSERT INTO `road_relation` VALUES ('HS002#0#04', 0, 'NS016#0#03', 3, 'HS002', 7);
INSERT INTO `road_relation` VALUES ('HS002#0#04', 1, 'NS015#0#03', 2, 'HS002', 9);
INSERT INTO `road_relation` VALUES ('HS002#0#04', 1, 'NS016#0#03', 3, 'HS002', 8);
INSERT INTO `road_relation` VALUES ('HS002#1#03', -1, 'NS021#0#01', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('HS002#1#04', -1, 'NS022#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('HS003#0#01', 0, 'HS003#1#04', 7, 'HS003', 7);
INSERT INTO `road_relation` VALUES ('HS003#0#01', 0, 'NS012#0#01', 3, 'HS003', 8);
INSERT INTO `road_relation` VALUES ('HS003#0#01', 0, 'NS013#0#03', 2, 'HS003', 9);
INSERT INTO `road_relation` VALUES ('HS003#0#02', 0, 'HS003#1#04', 3, 'HS003', 11);
INSERT INTO `road_relation` VALUES ('HS003#0#02', 0, 'NS011#0#03', 7, 'HS003', 10);
INSERT INTO `road_relation` VALUES ('HS003#0#02', 0, 'NS012#0#01', 2, 'HS003', 12);
INSERT INTO `road_relation` VALUES ('HS003#0#03', 0, 'HS003#1#04', 2, 'HS003', 3);
INSERT INTO `road_relation` VALUES ('HS003#0#03', 0, 'NS011#0#03', 3, 'HS003', 2);
INSERT INTO `road_relation` VALUES ('HS003#0#03', 0, 'NS013#0#03', 7, 'HS003', 1);
INSERT INTO `road_relation` VALUES ('HS003#0#04', 0, 'NS011#0#03', 2, 'HS003', 6);
INSERT INTO `road_relation` VALUES ('HS003#0#04', 0, 'NS012#0#01', 7, 'HS003', 4);
INSERT INTO `road_relation` VALUES ('HS003#0#04', 0, 'NS013#0#03', 3, 'HS003', 5);
INSERT INTO `road_relation` VALUES ('HS004#0#01', 0, 'HS004#1#03', 3, 'HS004', 6);
INSERT INTO `road_relation` VALUES ('HS004#0#01', 1, 'HS004#1#03', 3, 'HS004', 7);
INSERT INTO `road_relation` VALUES ('HS004#0#01', 1, 'NS011#0#01', 2, 'HS004', 8);
INSERT INTO `road_relation` VALUES ('HS004#0#02', 0, 'HS004#1#03', 2, 'HS004', 2);
INSERT INTO `road_relation` VALUES ('HS004#0#02', 0, 'NS008#0#03', 7, 'HS004', 1);
INSERT INTO `road_relation` VALUES ('HS004#0#03', 0, 'NS008#0#03', 3, 'HS004', 4);
INSERT INTO `road_relation` VALUES ('HS004#0#03', 0, 'NS011#0#01', 7, 'HS004', 3);
INSERT INTO `road_relation` VALUES ('HS004#0#03', 1, 'NS008#0#03', 3, 'HS004', 5);
INSERT INTO `road_relation` VALUES ('HS004#1#03', -1, 'NS010#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS001#0#01', 0, 'NS001#1#03', 3, 'NS001', 4);
INSERT INTO `road_relation` VALUES ('NS001#0#02', 0, 'NS001#1#03', 2, 'NS001', 5);
INSERT INTO `road_relation` VALUES ('NS001#0#03', 0, 'NS001#1#01', 3, 'NS001', 2);
INSERT INTO `road_relation` VALUES ('NS001#0#03', 0, 'NS001#1#02', 7, 'NS001', 1);
INSERT INTO `road_relation` VALUES ('NS001#0#03', 0, 'NS001#1#03', 11, 'NS001', 3);
INSERT INTO `road_relation` VALUES ('NS001#1#03', -1, 'NS002#0#01', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS002#0#01', 0, 'NS002#1#03', 3, 'NS002', 5);
INSERT INTO `road_relation` VALUES ('NS002#0#02', 0, 'NS002#1#03', 2, 'NS002', 1);
INSERT INTO `road_relation` VALUES ('NS002#0#03', 0, 'NS002#1#01', 3, 'NS002', 3);
INSERT INTO `road_relation` VALUES ('NS002#0#03', 0, 'NS002#1#02', 7, 'NS002', 2);
INSERT INTO `road_relation` VALUES ('NS002#0#03', 0, 'NS002#1#03', 11, 'NS002', 4);
INSERT INTO `road_relation` VALUES ('NS002#1#01', -1, 'NS001#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS002#1#03', -1, 'HS001#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS003#0#01', 0, 'NS007#0#01', 7, 'NS003', 4);
INSERT INTO `road_relation` VALUES ('NS003#0#01', 1, 'NS003#1#02', 2, 'NS003', 5);
INSERT INTO `road_relation` VALUES ('NS003#0#02', 0, 'NS003#1#01', 7, 'NS003', 6);
INSERT INTO `road_relation` VALUES ('NS003#0#02', 0, 'NS007#0#01', 3, 'NS003', 7);
INSERT INTO `road_relation` VALUES ('NS003#0#02', 1, 'NS007#0#01', 3, 'NS003', 8);
INSERT INTO `road_relation` VALUES ('NS003#0#03', 0, 'NS003#1#02', 3, 'NS003', 1);
INSERT INTO `road_relation` VALUES ('NS003#0#03', 1, 'NS003#1#01', 2, 'NS003', 3);
INSERT INTO `road_relation` VALUES ('NS003#0#03', 1, 'NS003#1#02', 3, 'NS003', 2);
INSERT INTO `road_relation` VALUES ('NS003#1#01', -1, 'NS004#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS003#1#02', -1, 'HS001#0#04', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS004#0#01', 0, 'NS004#1#02', 3, 'NS004', 6);
INSERT INTO `road_relation` VALUES ('NS004#0#01', 0, 'NS004#1#03', 7, 'NS004', 5);
INSERT INTO `road_relation` VALUES ('NS004#0#02', 0, 'NS004#1#01', 3, 'NS004', 1);
INSERT INTO `road_relation` VALUES ('NS004#0#02', 0, 'NS004#1#03', 2, 'NS004', 2);
INSERT INTO `road_relation` VALUES ('NS004#0#03', 0, 'NS004#1#01', 2, 'NS004', 4);
INSERT INTO `road_relation` VALUES ('NS004#0#03', 0, 'NS004#1#02', 3, 'NS004', 3);
INSERT INTO `road_relation` VALUES ('NS004#1#02', -1, 'NS003#0#01', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS004#1#03', -1, 'NS005#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS005#0#01', 0, 'NS005#1#02', 3, 'NS005', 4);
INSERT INTO `road_relation` VALUES ('NS005#0#02', 0, 'NS005#1#01', 3, 'NS005', 1);
INSERT INTO `road_relation` VALUES ('NS005#0#02', 0, 'NS006#0#01', 2, 'NS005', 2);
INSERT INTO `road_relation` VALUES ('NS005#0#03', 0, 'NS005#1#02', 7, 'NS005', 3);
INSERT INTO `road_relation` VALUES ('NS005#1#02', -1, 'NS004#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS006#0#01', 0, 'NS006#1#02', 2, 'NS006', 4);
INSERT INTO `road_relation` VALUES ('NS006#0#01', 0, 'NS006#1#03', 3, 'NS006', 3);
INSERT INTO `road_relation` VALUES ('NS006#0#02', 0, 'NS005#0#03', 7, 'NS006', 1);
INSERT INTO `road_relation` VALUES ('NS006#0#03', 0, 'NS005#0#03', 3, 'NS006', 2);
INSERT INTO `road_relation` VALUES ('NS007#0#01', 0, 'NS007#1#03', 3, 'NS007', 6);
INSERT INTO `road_relation` VALUES ('NS007#0#01', 1, 'NS007#1#02', 2, 'NS007', 8);
INSERT INTO `road_relation` VALUES ('NS007#0#01', 1, 'NS007#1#03', 3, 'NS007', 7);
INSERT INTO `road_relation` VALUES ('NS007#0#02', 0, 'NS003#0#03', 3, 'NS007', 1);
INSERT INTO `road_relation` VALUES ('NS007#0#02', 0, 'NS007#1#03', 2, 'NS007', 2);
INSERT INTO `road_relation` VALUES ('NS007#0#03', 0, 'NS003#0#03', 3, 'NS007', 4);
INSERT INTO `road_relation` VALUES ('NS007#0#03', 0, 'NS007#1#02', 7, 'NS007', 3);
INSERT INTO `road_relation` VALUES ('NS007#0#03', 1, 'NS003#0#03', 3, 'NS007', 5);
INSERT INTO `road_relation` VALUES ('NS007#1#03', -1, 'NS008#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS008#0#01', 0, 'HS004#0#01', 7, 'NS008', 4);
INSERT INTO `road_relation` VALUES ('NS008#0#01', 1, 'NS008#1#02', 2, 'NS008', 5);
INSERT INTO `road_relation` VALUES ('NS008#0#02', 0, 'HS004#0#01', 3, 'NS008', 7);
INSERT INTO `road_relation` VALUES ('NS008#0#02', 0, 'NS009#0#02', 7, 'NS008', 6);
INSERT INTO `road_relation` VALUES ('NS008#0#02', 1, 'HS004#0#01', 3, 'NS008', 8);
INSERT INTO `road_relation` VALUES ('NS008#0#03', 0, 'NS008#1#02', 3, 'NS008', 1);
INSERT INTO `road_relation` VALUES ('NS008#0#03', 1, 'NS008#1#02', 3, 'NS008', 2);
INSERT INTO `road_relation` VALUES ('NS008#0#03', 1, 'NS009#0#02', 2, 'NS008', 3);
INSERT INTO `road_relation` VALUES ('NS008#1#02', -1, 'NS007#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS009#0#01', 0, 'NS008#0#01', 3, 'NS009', 4);
INSERT INTO `road_relation` VALUES ('NS009#0#02', 0, 'NS009#1#01', 3, 'NS009', 3);
INSERT INTO `road_relation` VALUES ('NS009#0#02', 1, 'NS009#1#03', 2, 'NS009', 1);
INSERT INTO `road_relation` VALUES ('NS009#0#03', 0, 'NS008#0#01', 7, 'NS009', 2);
INSERT INTO `road_relation` VALUES ('NS010#0#01', 0, 'NS010#1#02', 2, 'NS010', 6);
INSERT INTO `road_relation` VALUES ('NS010#0#01', 1, 'NS010#1#02', 2, 'NS010', 7);
INSERT INTO `road_relation` VALUES ('NS010#0#02', 0, 'NS010#1#01', 7, 'NS010', 1);
INSERT INTO `road_relation` VALUES ('NS010#0#02', 1, 'NS010#1#01', 7, 'NS010', 2);
INSERT INTO `road_relation` VALUES ('NS010#0#02', 1, 'NS010#1#03', 2, 'NS010', 3);
INSERT INTO `road_relation` VALUES ('NS010#0#03', 0, 'NS010#1#02', 7, 'NS010', 4);
INSERT INTO `road_relation` VALUES ('NS010#0#03', 1, 'NS010#1#02', 7, 'NS010', 5);
INSERT INTO `road_relation` VALUES ('NS010#1#02', -1, 'HS004#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS011#0#01', 0, 'HS003#0#01', 3, 'NS011', 3);
INSERT INTO `road_relation` VALUES ('NS011#0#01', 0, 'NS011#1#02', 2, 'NS011', 4);
INSERT INTO `road_relation` VALUES ('NS011#0#02', 0, 'HS004#0#02', 7, 'NS011', 5);
INSERT INTO `road_relation` VALUES ('NS011#0#02', 0, 'NS011#1#02', 2, 'NS011', 6);
INSERT INTO `road_relation` VALUES ('NS011#0#03', 0, 'HS004#0#02', 3, 'NS011', 2);
INSERT INTO `road_relation` VALUES ('NS011#0#03', 0, 'NS011#1#02', 7, 'NS011', 1);
INSERT INTO `road_relation` VALUES ('NS012#0#01', 0, 'HS003#0#03', 11, 'NS012', 4);
INSERT INTO `road_relation` VALUES ('NS012#0#01', 0, 'NS012#1#02', 2, 'NS012', 3);
INSERT INTO `road_relation` VALUES ('NS012#0#01', 0, 'NS012#1#03', 3, 'NS012', 2);
INSERT INTO `road_relation` VALUES ('NS012#0#02', 0, 'HS003#0#03', 7, 'NS012', 5);
INSERT INTO `road_relation` VALUES ('NS012#0#03', 0, 'HS003#0#03', 3, 'NS012', 1);
INSERT INTO `road_relation` VALUES ('NS013#0#01', 0, 'HS003#0#02', 7, 'NS013', 3);
INSERT INTO `road_relation` VALUES ('NS013#0#01', 0, 'NS013#1#01', 11, 'NS013', 5);
INSERT INTO `road_relation` VALUES ('NS013#0#01', 0, 'NS013#1#02', 2, 'NS013', 4);
INSERT INTO `road_relation` VALUES ('NS013#0#02', 0, 'HS003#0#02', 3, 'NS013', 7);
INSERT INTO `road_relation` VALUES ('NS013#0#02', 0, 'NS013#1#01', 7, 'NS013', 6);
INSERT INTO `road_relation` VALUES ('NS013#0#03', 0, 'NS013#1#01', 2, 'NS013', 2);
INSERT INTO `road_relation` VALUES ('NS013#0#03', 0, 'NS013#1#02', 3, 'NS013', 1);
INSERT INTO `road_relation` VALUES ('NS013#1#02', -1, 'NS014#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS014#0#01', 0, 'NS014#1#02', 2, 'NS014', 6);
INSERT INTO `road_relation` VALUES ('NS014#0#01', 0, 'NS014#1#03', 3, 'NS014', 5);
INSERT INTO `road_relation` VALUES ('NS014#0#02', 0, 'NS014#1#03', 2, 'NS014', 2);
INSERT INTO `road_relation` VALUES ('NS014#0#02', 0, 'NS022#0#03', 7, 'NS014', 1);
INSERT INTO `road_relation` VALUES ('NS014#0#03', 0, 'NS014#1#02', 7, 'NS014', 3);
INSERT INTO `road_relation` VALUES ('NS014#0#03', 0, 'NS022#0#03', 3, 'NS014', 4);
INSERT INTO `road_relation` VALUES ('NS014#1#03', -1, 'NS013#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS015#0#01', 0, 'HS002#0#01', 3, 'NS015', 4);
INSERT INTO `road_relation` VALUES ('NS015#0#01', 1, 'HS002#0#01', 3, 'NS015', 5);
INSERT INTO `road_relation` VALUES ('NS015#0#01', 2, 'NS019#0#03', 2, 'NS015', 6);
INSERT INTO `road_relation` VALUES ('NS015#0#02', 0, 'HS001#0#03', 7, 'NS015', 7);
INSERT INTO `road_relation` VALUES ('NS015#0#02', 0, 'HS002#0#01', 2, 'NS015', 8);
INSERT INTO `road_relation` VALUES ('NS015#0#03', 0, 'NS019#0#03', 7, 'NS015', 1);
INSERT INTO `road_relation` VALUES ('NS015#0#03', 1, 'HS001#0#03', 3, 'NS015', 2);
INSERT INTO `road_relation` VALUES ('NS015#0#03', 2, 'HS001#0#03', 3, 'NS015', 3);
INSERT INTO `road_relation` VALUES ('NS016#0#01', 0, 'HS002#0#02', 3, 'NS016', 5);
INSERT INTO `road_relation` VALUES ('NS016#0#01', 1, 'HS002#0#02', 3, 'NS016', 6);
INSERT INTO `road_relation` VALUES ('NS016#0#02', 0, 'HS002#0#02', 2, 'NS016', 1);
INSERT INTO `road_relation` VALUES ('NS016#0#03', 0, 'NS016#1#02', 7, 'NS016', 2);
INSERT INTO `road_relation` VALUES ('NS016#0#03', 0, 'NS017#0#03', 3, 'NS016', 3);
INSERT INTO `road_relation` VALUES ('NS016#0#03', 1, 'NS017#0#03', 3, 'NS016', 4);
INSERT INTO `road_relation` VALUES ('NS016#1#02', -1, 'NS018#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS017#0#01', 0, 'NS016#0#01', 7, 'NS017', 4);
INSERT INTO `road_relation` VALUES ('NS017#0#01', 0, 'NS019#0#02', 11, 'NS017', 6);
INSERT INTO `road_relation` VALUES ('NS017#0#01', 0, 'NS020#0#03', 2, 'NS017', 5);
INSERT INTO `road_relation` VALUES ('NS017#0#02', 0, 'NS016#0#01', 3, 'NS017', 8);
INSERT INTO `road_relation` VALUES ('NS017#0#02', 0, 'NS019#0#02', 7, 'NS017', 7);
INSERT INTO `road_relation` VALUES ('NS017#0#02', 1, 'NS016#0#01', 3, 'NS017', 9);
INSERT INTO `road_relation` VALUES ('NS017#0#03', 0, 'NS020#0#03', 3, 'NS017', 1);
INSERT INTO `road_relation` VALUES ('NS017#0#03', 1, 'NS019#0#02', 2, 'NS017', 3);
INSERT INTO `road_relation` VALUES ('NS017#0#03', 1, 'NS020#0#03', 3, 'NS017', 2);
INSERT INTO `road_relation` VALUES ('NS018#0#01', 0, 'NS018#1#03', 7, 'NS018', 5);
INSERT INTO `road_relation` VALUES ('NS018#0#02', 0, 'NS018#1#03', 2, 'NS018', 1);
INSERT INTO `road_relation` VALUES ('NS018#0#03', 0, 'NS018#1#01', 2, 'NS018', 3);
INSERT INTO `road_relation` VALUES ('NS018#0#03', 0, 'NS018#1#02', 7, 'NS018', 2);
INSERT INTO `road_relation` VALUES ('NS018#0#03', 0, 'NS018#1#03', 11, 'NS018', 4);
INSERT INTO `road_relation` VALUES ('NS018#1#03', -1, 'NS016#0#02', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS019#0#01', 0, 'NS015#0#02', 7, 'NS019', 7);
INSERT INTO `road_relation` VALUES ('NS019#0#01', 0, 'NS017#0#01', 2, 'NS019', 8);
INSERT INTO `road_relation` VALUES ('NS019#0#01', 0, 'NS019#1#01', 11, 'NS019', 9);
INSERT INTO `road_relation` VALUES ('NS019#0#02', 0, 'NS015#0#02', 3, 'NS019', 2);
INSERT INTO `road_relation` VALUES ('NS019#0#02', 0, 'NS017#0#01', 11, 'NS019', 3);
INSERT INTO `road_relation` VALUES ('NS019#0#02', 0, 'NS019#1#01', 7, 'NS019', 1);
INSERT INTO `road_relation` VALUES ('NS019#0#03', 0, 'NS015#0#02', 11, 'NS019', 6);
INSERT INTO `road_relation` VALUES ('NS019#0#03', 0, 'NS017#0#01', 3, 'NS019', 4);
INSERT INTO `road_relation` VALUES ('NS019#0#03', 0, 'NS019#1#01', 2, 'NS019', 5);
INSERT INTO `road_relation` VALUES ('NS020#0#01', 0, 'NS017#0#02', 3, 'NS020', 5);
INSERT INTO `road_relation` VALUES ('NS020#0#01', 1, 'NS017#0#02', 3, 'NS020', 6);
INSERT INTO `road_relation` VALUES ('NS020#0#02', 0, 'NS017#0#02', 2, 'NS020', 1);
INSERT INTO `road_relation` VALUES ('NS020#0#03', 0, 'NS020#1#01', 3, 'NS020', 3);
INSERT INTO `road_relation` VALUES ('NS020#0#03', 0, 'NS020#1#02', 7, 'NS020', 2);
INSERT INTO `road_relation` VALUES ('NS020#0#03', 1, 'NS020#1#01', 3, 'NS020', 4);
INSERT INTO `road_relation` VALUES ('NS021#0#01', 0, 'NS021#1#03', 3, 'NS021', 10);
INSERT INTO `road_relation` VALUES ('NS021#0#01', 0, 'NS021#1#04', 7, 'NS021', 9);
INSERT INTO `road_relation` VALUES ('NS021#0#01', 1, 'NS021#1#03', 3, 'NS021', 11);
INSERT INTO `road_relation` VALUES ('NS021#0#01', 2, 'NS021#1#02', 2, 'NS021', 13);
INSERT INTO `road_relation` VALUES ('NS021#0#01', 2, 'NS021#1#03', 3, 'NS021', 12);
INSERT INTO `road_relation` VALUES ('NS021#0#02', 0, 'NS021#1#01', 7, 'NS021', 14);
INSERT INTO `road_relation` VALUES ('NS021#0#02', 0, 'NS021#1#03', 2, 'NS021', 16);
INSERT INTO `road_relation` VALUES ('NS021#0#02', 0, 'NS021#1#04', 1, 'NS021', 15);
INSERT INTO `road_relation` VALUES ('NS021#0#03', 0, 'NS021#1#01', 3, 'NS021', 2);
INSERT INTO `road_relation` VALUES ('NS021#0#03', 0, 'NS021#1#02', 7, 'NS021', 1);
INSERT INTO `road_relation` VALUES ('NS021#0#03', 1, 'NS021#1#01', 3, 'NS021', 3);
INSERT INTO `road_relation` VALUES ('NS021#0#03', 2, 'NS021#1#01', 3, 'NS021', 4);
INSERT INTO `road_relation` VALUES ('NS021#0#03', 2, 'NS021#1#04', 2, 'NS021', 5);
INSERT INTO `road_relation` VALUES ('NS021#0#04', 0, 'NS021#1#01', 2, 'NS021', 8);
INSERT INTO `road_relation` VALUES ('NS021#0#04', 0, 'NS021#1#02', 3, 'NS021', 7);
INSERT INTO `road_relation` VALUES ('NS021#0#04', 0, 'NS021#1#03', 7, 'NS021', 6);
INSERT INTO `road_relation` VALUES ('NS021#1#01', -1, 'HS002#0#03', 0, '0', 0);
INSERT INTO `road_relation` VALUES ('NS022#0#01', 0, 'NS014#0#01', 7, 'NS022', 3);
INSERT INTO `road_relation` VALUES ('NS022#0#01', 0, 'NS022#1#02', 2, 'NS022', 4);
INSERT INTO `road_relation` VALUES ('NS022#0#02', 0, 'NS014#0#01', 3, 'NS022', 6);
INSERT INTO `road_relation` VALUES ('NS022#0#02', 0, 'NS022#1#01', 7, 'NS022', 5);
INSERT INTO `road_relation` VALUES ('NS022#0#03', 0, 'NS022#1#01', 2, 'NS022', 2);
INSERT INTO `road_relation` VALUES ('NS022#0#03', 0, 'NS022#1#02', 3, 'NS022', 1);
INSERT INTO `road_relation` VALUES ('NS022#1#02', -1, 'HS002#0#04', 0, '0', 0);

-- ----------------------------
-- Table structure for signal_phases
-- ----------------------------
DROP TABLE IF EXISTS `signal_phases`;
CREATE TABLE `signal_phases`  (
  `INTERSECTION_ID` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TOTAL_PHASES` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`INTERSECTION_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of signal_phases
-- ----------------------------
INSERT INTO `signal_phases` VALUES ('HS001', 8);
INSERT INTO `signal_phases` VALUES ('HS002', 8);
INSERT INTO `signal_phases` VALUES ('HS003', 8);
INSERT INTO `signal_phases` VALUES ('HS004', 6);
INSERT INTO `signal_phases` VALUES ('NS001', 0);
INSERT INTO `signal_phases` VALUES ('NS002', 0);
INSERT INTO `signal_phases` VALUES ('NS003', 0);
INSERT INTO `signal_phases` VALUES ('NS004', 0);
INSERT INTO `signal_phases` VALUES ('NS005', 0);
INSERT INTO `signal_phases` VALUES ('NS006', 0);
INSERT INTO `signal_phases` VALUES ('NS007', 0);
INSERT INTO `signal_phases` VALUES ('NS008', 0);
INSERT INTO `signal_phases` VALUES ('NS009', 0);
INSERT INTO `signal_phases` VALUES ('NS010', 0);
INSERT INTO `signal_phases` VALUES ('NS011', 0);
INSERT INTO `signal_phases` VALUES ('NS012', 0);
INSERT INTO `signal_phases` VALUES ('NS013', 0);
INSERT INTO `signal_phases` VALUES ('NS014', 0);
INSERT INTO `signal_phases` VALUES ('NS015', 0);
INSERT INTO `signal_phases` VALUES ('NS016', 0);
INSERT INTO `signal_phases` VALUES ('NS017', 0);
INSERT INTO `signal_phases` VALUES ('NS018', 0);
INSERT INTO `signal_phases` VALUES ('NS019', 0);
INSERT INTO `signal_phases` VALUES ('NS020', 0);
INSERT INTO `signal_phases` VALUES ('NS021', 0);
INSERT INTO `signal_phases` VALUES ('NS022', 0);

SET FOREIGN_KEY_CHECKS = 1;
