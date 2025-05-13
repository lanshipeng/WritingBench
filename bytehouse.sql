-- 用户统计表
CREATE TABLE IF NOT EXISTS user_stats (
    optimizer_id Int64 COMMENT '优化师ID',

    daily_active_user_count Int32 COMMENT '当日活跃用户数',
    recharge_user_count Int32 COMMENT '充值用户数',
    recharge_amount Decimal(20, 2) COMMENT '充值总金额',
    recharge_rate String COMMENT '充值率',
    daily_active_recharge_amount Decimal(20, 2) COMMENT '活跃用户充值金额',
    new_registered_user_count Int32 COMMENT '新注册用户数',
    new_recharge_user_count Int32 COMMENT '新充值用户数',
    new_recharge_users_recharge_amount Decimal(20, 2) COMMENT '新充值用户的充值总金额',
    new_users_avg_recharge_amount Decimal(20, 2) COMMENT '新用户平均充值金额',
    new_recharge_rate String COMMENT '新充值率',

    create_time DateTime COMMENT '创建时间',
    update_time DateTime COMMENT '更新时间'
) ENGINE = MergeTree()
ORDER BY (optimizer_id, create_time);

--  #"http://192.168.10.15:8000/v1/chat/completions"
-- 广告投放收益统计表
CREATE TABLE IF NOT EXISTS ad_performance_stats
(
    optimizer_id             String COMMENT '优化器ID',
    media                    String COMMENT '媒体',
    ad_account_id            String COMMENT '广告账户ID',
    ad_account_name          String COMMENT '广告账户名称',
    ad_sequence              String COMMENT '广告序列号',
    ad_unit                  String COMMENT '广告单元',
    ad_id                    String COMMENT '广告ID',
    spend                    Int32  COMMENT '消耗',
    recharge_amount          Int32  COMMENT '充值金额',
    roi                      String COMMENT 'ROI',
    impressions_user_count   Int32  COMMENT '曝光用户数',
    clicks_user_count        Int32  COMMENT '点击用户数',
    click_rate               String COMMENT '点击率',
    new_user_count           Int32  COMMENT '新增用户数',
    call_up_user_count       Int32  COMMENT '拉起用户数',
    new_call_up_rate         String COMMENT '新增拉起率',
    pay_impressions_user_count Int32 COMMENT '付费曝光用户数',
    pay_user_count           Int32  COMMENT '付费用户数',
    d1_pay_amount            Int32  COMMENT '次日付费金额',
    d2_pay_amount            Int32  COMMENT '2日付费金额',
    d3_pay_amount            Int32  COMMENT '3日付费金额',
    d7_pay_amount            Int32  COMMENT '7日付费金额',
    d14_pay_amount           Int32  COMMENT '14日付费金额',
    d30_pay_amount           Int32  COMMENT '30日付费金额',
    d45_pay_amount           Int32  COMMENT '45日付费金额',
    d60_pay_amount           Int32  COMMENT '60日付费金额',

    create_time DateTime COMMENT '创建时间',
    update_time DateTime COMMENT '更新时间'
)
ENGINE = MergeTree
ORDER BY (create_time, optimizer_id, ad_id);

-- 短剧统计表
CREATE TABLE IF NOT EXISTS drama_stats (
    drama_id Int64 COMMENT '剧集ID',
    drama_name String COMMENT '剧集名称',
    drama_alias String COMMENT '剧集别名',
    launch_time String COMMENT '上线时间',
    launch_days Int32 COMMENT '上线天数',
    start_play_count Int32 COMMENT '开始播放数',
    valid_play_count Int32 COMMENT '有效播放数',
    total_income Decimal(20, 2) COMMENT '总收入',
    newly_attributed_revenue Decimal(20, 2) COMMENT '新增归因收入',
    unlock_expose_count Int32 COMMENT '解锁曝光次数',
    unlock_recharge_people_count Int32 COMMENT '解锁充值人数',
    unlock_recharge_count Int32 COMMENT '解锁充值次数',
    start_play_recharge_rate String COMMENT '开始播放转化率',
    arpu Decimal(20, 2) COMMENT '每用户平均收入',
    total_ad_spent Decimal(20, 2) COMMENT '广告支出',
    total_roi String COMMENT 'ROI',
    collection_count Int32 COMMENT '收藏数',

    create_time DateTime COMMENT '创建时间',
    update_time DateTime COMMENT '更新时间'
) ENGINE = MergeTree()
ORDER BY (drama_id,create_time);

-- 剧集章节统计表
CREATE TABLE IF NOT EXISTS drama_episode_stats (
    drama_id Int64 COMMENT '剧集ID',
    episode_index Int32 COMMENT '剧集索引',
    is_free UInt8 COMMENT '是否免费',
    start_play_count Int32 COMMENT '开始播放次数',
    first_play_rate String COMMENT '首集播放留存率',
    play_rate String COMMENT '播放留存率',
    start_play_user_count Int32 COMMENT '开始播放用户数',
    unlock_user_count Int32 COMMENT '解锁用户数',
    unlock_user_pay_count Int32 COMMENT '解锁付费用户数',
    unlock_user_ad_count Int32 COMMENT '解锁广告用户数',
    unlock_user_vip_count Int32 COMMENT '解锁VIP用户数',
    recharge_user_count Int32 COMMENT '充值用户数',
    unlock_user_recharge_count Int32 COMMENT '解锁用户充值次数',
    vip_recharge_count Int32 COMMENT 'VIP充值次数',
    user_recharge_count Int32 COMMENT '用户充值次数',
    recharge_coins Int32 COMMENT '充值金币数',
    unlock_recharge_coins Int32 COMMENT '解锁充值金币数',
    vip_recharge_coins Int32 COMMENT 'VIP充值金币数',
    user_recharge_coins Int32 COMMENT '用户充值金币数',
    valid_play_user_count Int32 COMMENT '有效播放用户数',
    valid_play_count Int32 COMMENT '有效播放次数',
    avg_play_duration Int32 COMMENT '平均播放时长（秒）',
    complete_play_user_count Int32 COMMENT '完整观看用户数',
    complete_play_count Int32 COMMENT '完整观看次数',
    complete_play_rate String COMMENT '完整播放率',

    create_time DateTime COMMENT '创建时间',
    update_time DateTime COMMENT '更新时间'
) ENGINE = MergeTree()
ORDER BY (drama_id, episode_index,create_time);

-- 回收趋势统计表
CREATE TABLE IF NOT EXISTS recycle_trend_stats (
    drama_id Int64 COMMENT '剧集ID',
    drama_name String COMMENT '剧集名称',
    drama_alias String COMMENT '剧集别名',
    consume Int32 COMMENT '消耗',
    attribution_added_income Int32 COMMENT '归因新增收益',
    total_roi String COMMENT '整体ROI',
    new_user_count Int32 COMMENT '新增用户数',
    new_user_launch_count Int32 COMMENT '新增用户启动数',
    launch_rate String COMMENT '启动率',
    recharge_expose_count Int32 COMMENT '曝光充值次数',
    total_recharge_count Int32 COMMENT '总充值次数',
    recharge_rate String COMMENT '充值率',
    new_user_expense Int32 COMMENT '新增用户消耗',
    recharge_expense Int32 COMMENT '充值消耗',
    new_user_avg_recharge_amo Int32 COMMENT '新增用户人均充值金额',
    recharge_avg_recharge Int32 COMMENT '充值人均金额',

    d1_recharge_amount Int32,
    d1_roi String,
    d2_recharge_amount Int32,
    d2_roi String,
    d2_roi_incr_speed String,
    d3_recharge_amount Int32,
    d3_roi String,
    d3_roi_incr_speed String,
    d4_recharge_amount Int32,
    d4_roi String,
    d4_roi_incr_speed String,
    d5_recharge_amount Int32,
    d5_roi String,
    d5_roi_incr_speed String,
    d6_recharge_amount Int32,
    d6_roi String,
    d6_roi_incr_speed String,
    d7_recharge_amount Int32,
    d7_roi String,
    d7_roi_incr_speed String,
    d8_recharge_amount Int32,
    d8_roi String,
    d8_roi_incr_speed String,
    d15_recharge_amount Int32,
    d15_roi String,
    d15_roi_incr_speed String,
    d22_recharge_amount Int32,
    d22_roi String,
    d22_roi_incr_speed String,
    d30_recharge_amount Int32,
    d30_roi String,
    d30_roi_incr_speed String,
    d45_recharge_amount Int32,
    d45_roi String,
    d45_roi_incr_speed String,
    d60_recharge_amount Int32,
    d60_roi String,
    d60_roi_incr_speed String,
    d90_recharge_amount Int32,
    d90_roi String,
    d90_roi_incr_speed String,

    create_time DateTime COMMENT '创建时间',
    update_time DateTime COMMENT '更新时间'
) ENGINE = MergeTree()
ORDER BY (drama_id, create_time);
