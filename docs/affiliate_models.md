
AffiliateAudit(referral_codes [AffiliateCode], action_taken, action_date, user [User], ip_address, device_info, location)
 
AffiliateCampaign(programs [AffiliateProgram], campaign_name, start_date, end_date, goal, budget, spending_to_date, target_audience)

AffiliateCommission(affiliates [Affiliate], programs [AffiliateProgram], amount, currency, date_awarded, status, approved_by, commission_type, description, tier) 

AffiliateIncentive(affiliate, program, incentive_type, date, amount, currency, status, description, ip_address, device_info, tracking_id, expiration_date is_incentive_active)

AffiliateLink(affiliates [Affiliate], programs [AffiliateProgram], url, click_count, conversion_count, date_created, last_used, link_status, landing_page, custom_tracking_id)

AffiliateNotification(user [User], message, date_sent, is_read, notification_type, priority, action_required)

AffiliatePayout(affiliates [Affiliate], amount, currency, payout_date, payout_method, payout_status, transaction_id, processing_fee, net_amount, payout_provider)

AffiliateProgramPartecipation(referral_codes, programs, date_joined, reward_earned, status)

AffiliateProgram(name, description, reward_type, reward_value, currency, min_referral_count, max_referrals_per_user, date_created, is_active, program_duration, allowed_regions, target_industry)

AffiliateReward(referral_codes [AffiliateCode], referred_user [User], reward_type, reward_value, date_awarded, status, expiry_date, reward_description, reward_source)

AffiliateSettings(user [User], default_reward_type, max_referrals_allowed, notification_preference, auto_share_setting, social_share_message)

AffiliateSupportTicket(affiliates [Affiliate], ticket_number, subject, description, status, date_created, date_closed, priority, assigned_agent)

AffiliateTier(programs [AffiliateProgram], tier_name, min_sales, commission_rate, tier_benefits, access_level, next_tier_threshold, tier_expiration)

AffiliateTransaction(referral_codes [AffiliateCode], referred_user [User], transaction_date, order_id, transaction_amount, currency, status, conversion_value, discount_value, coupon_code_used, channel)
