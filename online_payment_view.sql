CREATE
OR REPLACE
VIEW `bhmc`.`online_payment_view` AS select
    `e`.`id` AS `event_id`,
    `e`.`name` AS `name`,
    `e`.`event_type` AS `event_type`,
    `e`.`start_date` AS `start_date`,
    `g`.`signed_up_by_id` AS `signed_up_by_id`,
    `u`.`first_name` AS `first_name`,
    `u`.`last_name` AS `last_name`,
    `g`.`payment_amount` AS `payment_amount`,
    `g`.`payment_confirmation_code` AS `payment_confirmation_code`,
    `g`.`payment_confirmation_timestamp` AS `payment_confirmation_timestamp`,
    `r`.`refund_code` AS `refund_code`,
    `r`.`refund_timestamp` AS `refund_timestamp`,
    `r`.`refund_amount` AS `refund_amount`,
    `r`.`comment` AS `comment`,
    concat_ws(' ',
    `ru`.`first_name`,
    `ru`.`last_name`) AS `refunded_by`,
    `g`.`id` AS `record_id`,
    'group-payment' AS `record_type`,
    concat(`g`.`id`,
    'g') AS `pkey`
from
    ((((((`bhmc`.`events_event` `e`
join `bhmc`.`register_registrationgroup` `g` on
    ((`e`.`id` = `g`.`event_id`)))
join `bhmc`.`core_member` `m` on
    ((`g`.`signed_up_by_id` = `m`.`id`)))
join `bhmc`.`auth_user` `u` on
    ((`m`.`user_id` = `u`.`id`)))
left join `bhmc`.`register_registrationrefund` `r` on
    ((`g`.`id` = `r`.`related_record_id`)))
left join `bhmc`.`core_member` `rm` on
    ((`r`.`recorded_by_id` = `rm`.`id`)))
left join `bhmc`.`auth_user` `ru` on
    ((`rm`.`user_id` = `ru`.`id`)))
where
    (`g`.`payment_confirmation_code` like 'ch_%')
union all select
    `e`.`id` AS `event_id`,
    `e`.`name` AS `name`,
    `e`.`event_type` AS `event_type`,
    `e`.`start_date` AS `start_date`,
    `p`.`recorded_by_id` AS `recorded_by_id`,
    `u`.`first_name` AS `first_name`,
    `u`.`last_name` AS `last_name`,
    `p`.`payment_amount` AS `payment_amount`,
    `p`.`payment_code` AS `payment_code`,
    `p`.`payment_timestamp` AS `payment_timestamp`,
    `r`.`refund_code` AS `refund_code`,
    `r`.`refund_timestamp` AS `refund_timestamp`,
    `r`.`refund_amount` AS `refund_amount`,
    `r`.`comment` AS `comment`,
    concat_ws(' ',
    `ru`.`first_name`,
    `ru`.`last_name`) AS `refunded_by`,
    `p`.`id` AS `record_id`,
    'slot-payment' AS `record_type`,
    concat(`p`.`id`,
    'p') AS `pkey`
from
    (((((((`bhmc`.`events_event` `e`
join `bhmc`.`register_registrationslot` `s` on
    ((`e`.`id` = `s`.`event_id`)))
join `bhmc`.`register_registrationslotpayment` `p` on
    ((`s`.`id` = `p`.`registration_slot_id`)))
join `bhmc`.`core_member` `m` on
    ((`p`.`recorded_by_id` = `m`.`id`)))
join `bhmc`.`auth_user` `u` on
    ((`m`.`user_id` = `u`.`id`)))
left join `bhmc`.`register_registrationrefund` `r` on
    ((`s`.`id` = `r`.`related_record_id`)))
left join `bhmc`.`core_member` `rm` on
    ((`r`.`recorded_by_id` = `rm`.`id`)))
left join `bhmc`.`auth_user` `ru` on
    ((`rm`.`user_id` = `ru`.`id`)))
where
    (`p`.`payment_code` like 'ch_%');
