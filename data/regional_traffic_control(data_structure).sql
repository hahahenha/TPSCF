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

 Date: 06/09/2022 14:54:25
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
  PRIMARY KEY (`INTERSECTION_ID`, `PHASE_NUM`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for road_lanes
-- ----------------------------
DROP TABLE IF EXISTS `road_lanes`;
CREATE TABLE `road_lanes`  (
  `ROAD_ID_FROM` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `LANE_NUM` int(11) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

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
-- Table structure for signal_phases
-- ----------------------------
DROP TABLE IF EXISTS `signal_phases`;
CREATE TABLE `signal_phases`  (
  `INTERSECTION_ID` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TOTAL_PHASES` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`INTERSECTION_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
