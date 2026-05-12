create extension if not exists pg_cron with schema pg_catalog;
create extension if not exists pgcrypto with schema extensions;

create table if not exists public.app_settings (
    key text primary key,
    value jsonb not null,
    updated_at timestamptz not null default now(),
    constraint app_settings_key_format_chk check (key ~ '^[a-z0-9_]+$')
);

alter table public.app_settings enable row level security;

insert into public.app_settings (key, value)
values ('log_retention_days', '30'::jsonb)
on conflict (key) do nothing;

create table if not exists public.app_events (
    id uuid primary key default gen_random_uuid(),
    created_at timestamptz not null default now(),
    event_name text not null,
    event_category text not null,
    route text,
    method text,
    status_code integer,
    duration_ms integer,
    request_id text,
    actor_type text,
    actor_id text,
    ip_hash text,
    user_agent text,
    metadata jsonb not null default '{}'::jsonb,
    constraint app_events_event_name_chk check (length(btrim(event_name)) > 0),
    constraint app_events_event_category_chk check (length(btrim(event_category)) > 0),
    constraint app_events_status_code_chk check (status_code is null or status_code between 100 and 599),
    constraint app_events_duration_ms_chk check (duration_ms is null or duration_ms >= 0),
    constraint app_events_metadata_object_chk check (jsonb_typeof(metadata) = 'object')
);

alter table public.app_events enable row level security;

create index if not exists app_events_created_at_idx on public.app_events (created_at desc);
create index if not exists app_events_event_name_created_at_idx on public.app_events (event_name, created_at desc);
create index if not exists app_events_event_category_created_at_idx on public.app_events (event_category, created_at desc);
create index if not exists app_events_request_id_idx on public.app_events (request_id) where request_id is not null;

create schema if not exists internal;

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
    from public.app_settings
    where key = 'log_retention_days';

    retention_days := coalesce(retention_days, 30);

    if retention_days < 1 then
        raise exception 'log_retention_days must be greater than zero';
    end if;

    delete from public.app_events
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
