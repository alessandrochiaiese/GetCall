
ReferralAudit(referral_codes [ReferralCode], action_taken, action_date, user [User], ip_address, device_info, location)

ReferralBonus(programs [ReferralProgram], bonus_type, bonus_value, min_referrals_required, bonus_date, expiry_date, max_usage, eligibility_criteria)

ReferralCampaign(programs [ReferralProgram], campaign_name, start_date, end_date, goal, budget, spending_to_date, target_audience)

ReferralCode(user [User], programs [ReferralProgram], code, usage_count, date_created, status, expiry_date, referred_user_count, unique_url, campaign_source, campaign_medium)

ReferralConversion(referral_codes [ReferralCode], referred_user [User], conversion_date, conversion_value, status, reward_issued, conversion_source, referral_type)

ReferralEngagement(referral_codes [ReferralCode], user [User], email_opened, email_clicked, social_share_count, last_interaction_date)

ReferralNotification(user [User], message, date_sent, is_read, notification_type, priority, action_required)

ReferralProgramPartecipation(referral_codes, programs, date_joined, reward_earned, status)

ReferralProgram(name, description, reward_type, reward_value, currency, min_referral_count, max_referrals_per_user, date_created, is_active, program_duration, allowed_regions, target_industry)

ReferralReward(referral_codes [ReferralCode], referred_user [User], reward_type, reward_value, date_awarded, status, expiry_date, reward_description, reward_source)

ReferralSettings(user [User], default_reward_type, max_referrals_allowed, notification_preference, auto_share_setting, social_share_message)

ReferralStats(referral_codes [ReferralCode], period, click_count, conversion_count, total_rewards, average_conversion_value, highest_referral_earning)

ReferralTransaction(referral_codes [ReferralCode], referred_user [User], transaction_date, order_id, transaction_amount, currency, status, conversion_value, discount_value, coupon_code_used, channel)

ReferralUser(user [User], total_referrals, active_referrals, inactive_referrals, total_rewards_earned, total_spent_by_referred_users, average_order_value, loyalty_points_earned)

Referral(program, referrer, referred, reward_given)
 