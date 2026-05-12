create schema if not exists internal;

alter table if exists public.app_settings set schema internal;
alter table if exists public.app_events set schema internal;

create or replace function internal.cleanup_app_events()
returns integer
language plpgsql
set search_path = ''
as $$
declare
    retention_days integer;
    deleted_count integer;
begin
    select nullif(value #>> '{}', '')::integer
    into retention_days
    from internal.app_settings
    where key = 'log_retention_days';

    retention_days := coalesce(retention_days, 30);

    if retention_days < 1 then
        raise exception 'log_retention_days must be greater than zero';
    end if;

    delete from internal.app_events
    where created_at < now() - make_interval(days => retention_days);

    get diagnostics deleted_count = row_count;
    return deleted_count;
end;
$$;

do $$
begin
    if exists (select 1 from cron.job where jobname = 'cleanup-app-events') then
        perform cron.unschedule('cleanup-app-events');
    end if;
end;
$$;

select cron.schedule(
    'cleanup-app-events',
    '17 3 * * *',
    $$select internal.cleanup_app_events();$$
);
