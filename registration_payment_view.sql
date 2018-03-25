ALTER VIEW club.online_payment_view AS
SELECT
   e.id AS event_id
  ,e.name
  ,e.event_type
  ,e.start_date
  ,g.signed_up_by_id
  ,u.first_name
  ,u.last_name
  ,g.payment_amount
  ,g.payment_confirmation_code
  ,g.payment_confirmation_timestamp
  ,g.id AS record_id
  ,'group-payment' AS record_type
  ,concat(g.id, 'g') AS pkey
FROM club.events_event AS e
JOIN club.register_registrationgroup AS g ON e.id = g.event_id
JOIN club.core_member AS m ON g.signed_up_by_id = m.id
JOIN club.auth_user AS u ON m.user_id = u.id
WHERE g.payment_confirmation_code LIKE 'ch_%'
UNION ALL
SELECT
   e.id AS event_id
  ,e.name
  ,e.event_type
  ,e.start_date
  ,p.recorded_by_id
  ,u.first_name
  ,u.last_name
  ,p.payment_amount
  ,p.payment_code
  ,p.payment_timestamp
  ,p.id AS record_id
  ,'slot-payment' AS record_type
  ,concat(p.id, 'p') AS pkey
FROM club.events_event AS e
JOIN club.register_registrationslot AS s ON e.id = s.event_id
JOIN club.register_registrationslotpayment AS p ON s.id = p.registration_slot_id
JOIN club.core_member AS m ON p.recorded_by_id = m.id
JOIN club.auth_user AS u ON m.user_id = u.id
WHERE p.payment_code LIKE 'ch_%'

