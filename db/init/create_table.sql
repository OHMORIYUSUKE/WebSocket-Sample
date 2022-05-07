-- アイドルマスター キャラクターデータ
SET NAMES utf8;
USE `fuel_dev`;

-- 既存テーブルの削除
DROP TABLE IF EXISTS `message`;

-- テーブル定義
CREATE TABLE IF NOT EXISTS `message`(
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '連番ID',
    `message` VARCHAR(100) NOT NULL COMMENT "メッセージ",
    PRIMARY KEY(`id`)
)