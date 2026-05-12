create policy app_events_postgres_all
on internal.app_events
for all
to postgres
using (true)
with check (true);

create policy app_settings_postgres_all
on internal.app_settings
for all
to postgres
using (true)
with check (true);
