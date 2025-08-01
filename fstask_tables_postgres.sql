--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: trigger_fct_tib_fs_job_handler(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trigger_fct_tib_fs_job_handler() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
    errno            numeric;
    errmsg           char(200);
    dummy            numeric;
BEGIN
  BEGIN
    --  Column ""id"" uses sequence S_FS_JOB_HANDLER
    select nextval('s_fs_job_handler') INTO STRICT NEW.id;
--  Errors handling
exception
    when SQLSTATE '50001' then
       RAISE EXCEPTION '%', errmsg USING ERRCODE = errno;
  END;
RETURN NEW;
end
$$;



--
-- Name: trigger_fct_tib_fs_trigger_registry(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trigger_fct_tib_fs_trigger_registry() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
    errno            numeric;
    errmsg           char(200);
    dummy            numeric;
BEGIN
  BEGIN
    --  Column ""id"" uses sequence S_FS_TRIGGER_REGISTRY
    select nextval('s_fs_trigger_registry') INTO STRICT NEW.id;
--  Errors handling
exception
    when SQLSTATE '50001' then
       RAISE EXCEPTION '%', errmsg USING ERRCODE = errno;
  END;
RETURN NEW;
end
$$;



SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: fs_blob_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_blob_triggers (
    sched_name character varying(120) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    blob_data bytea
);



--
-- Name: fs_calendars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_calendars (
    sched_name character varying(120) NOT NULL,
    calendar_name character varying(200) NOT NULL,
    calendar bytea NOT NULL
);



--
-- Name: fs_cron_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_cron_triggers (
    sched_name character varying(120) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    cron_expression character varying(120) NOT NULL,
    time_zone_id character varying(80)
);



--
-- Name: fs_dfc_job_handler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_dfc_job_handler (
    id integer NOT NULL,
    executorid integer NOT NULL,
    handlername character varying(50) NOT NULL,
    injecttype integer DEFAULT 1 NOT NULL,
    strategy integer DEFAULT 1 NOT NULL,
    strategyparam character varying(30)
);



--
-- Name: fs_dfc_job_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_dfc_job_info (
    id integer NOT NULL,
    job_group integer NOT NULL,
    job_cron character varying(4000),
    job_desc character varying(4000) NOT NULL,
    add_time timestamp without time zone,
    update_time timestamp without time zone,
    author character varying(4000),
    alarm_email character varying(4000),
    executor_route_strategy character varying(4000),
    executor_handler character varying(4000),
    executor_param character varying(4000),
    executor_block_strategy character varying(4000),
    executor_fail_strategy character varying(4000),
    executor_timeout integer DEFAULT 0,
    glue_type character varying(4000) NOT NULL,
    glue_source text,
    glue_remark character varying(4000),
    glue_updatetime timestamp without time zone,
    child_jobkey character varying(4000),
    resulttype character varying(4000) DEFAULT 'param'::character varying,
    depend_job_result character varying(100),
    taskid integer,
    job_order_in_task integer,
    job_name character varying(100) DEFAULT ('job_'::text || LOCALTIMESTAMP) NOT NULL
);



--
-- Name: COLUMN fs_dfc_job_info.job_group; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_dfc_job_info.job_group IS '也就是对应的executor的 id';


--
-- Name: COLUMN fs_dfc_job_info.resulttype; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_dfc_job_info.resulttype IS '返回结果类型 ''param''/''table''/..';


--
-- Name: COLUMN fs_dfc_job_info.depend_job_result; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_dfc_job_info.depend_job_result IS '依赖前序 job order 的结果作为参数';


--
-- Name: COLUMN fs_dfc_job_info.taskid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_dfc_job_info.taskid IS '所属 taskid';


--
-- Name: COLUMN fs_dfc_job_info.job_order_in_task; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_dfc_job_info.job_order_in_task IS '当前 job 在 task 中的执行顺序';


--
-- Name: fs_dfc_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_dfc_tasks (
    id integer NOT NULL,
    author character varying(100) NOT NULL,
    task_name character varying(40) NOT NULL,
    task_uuid character varying(140),
    user_identity character varying(140),
    listener_name character varying(140),
    task_cron character varying(100),
    description character varying(4000) NOT NULL,
    remark character varying(10),
    task_level character varying(40)
);



--
-- Name: fs_fired_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_fired_triggers (
    sched_name character varying(120) NOT NULL,
    entry_id character varying(95) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    instance_name character varying(200) NOT NULL,
    fired_time bigint NOT NULL,
    sched_time bigint NOT NULL,
    priority integer NOT NULL,
    state character varying(16) NOT NULL,
    job_name character varying(200),
    job_group character varying(200),
    is_nonconcurrent boolean,
    requests_recovery boolean
);



--
-- Name: fs_job_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_job_details (
    sched_name character varying(120) NOT NULL,
    job_name character varying(200) NOT NULL,
    job_group character varying(200) NOT NULL,
    description character varying(250),
    job_class_name character varying(250) NOT NULL,
    is_durable boolean NOT NULL,
    is_nonconcurrent boolean NOT NULL,
    is_update_data boolean NOT NULL,
    requests_recovery boolean NOT NULL,
    job_data bytea
);



--
-- Name: fs_locks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_locks (
    sched_name character varying(120) NOT NULL,
    lock_name character varying(40) NOT NULL
);



--
-- Name: fs_paused_trigger_grps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_paused_trigger_grps (
    sched_name character varying(120) NOT NULL,
    trigger_group character varying(200) NOT NULL
);



--
-- Name: fs_scheduler_state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_scheduler_state (
    sched_name character varying(120) NOT NULL,
    instance_name character varying(200) NOT NULL,
    last_checkin_time bigint NOT NULL,
    checkin_interval bigint NOT NULL
);



--
-- Name: fs_simple_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_simple_triggers (
    sched_name character varying(120) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    repeat_count bigint NOT NULL,
    repeat_interval bigint NOT NULL,
    times_triggered bigint NOT NULL
);



--
-- Name: fs_simprop_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_simprop_triggers (
    sched_name character varying(120) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    str_prop_1 character varying(512),
    str_prop_2 character varying(512),
    str_prop_3 character varying(512),
    int_prop_1 integer,
    int_prop_2 integer,
    long_prop_1 bigint,
    long_prop_2 bigint,
    dec_prop_1 numeric(13,4),
    dec_prop_2 numeric(13,4),
    bool_prop_1 boolean,
    bool_prop_2 boolean
);



--
-- Name: fs_trigger_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_trigger_group (
    id integer NOT NULL,
    app_name character varying(4000) NOT NULL,
    title character varying(4000) NOT NULL,
    group_order integer DEFAULT 0 NOT NULL,
    address_type integer DEFAULT 0 NOT NULL,
    address_list character varying(4000)
);



--
-- Name: fs_trigger_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_trigger_log (
    id integer NOT NULL,
    job_group integer NOT NULL,
    job_id integer NOT NULL,
    glue_type character varying(50),
    log_locate character varying(50),
    executor_address character varying(255),
    executor_handler character varying(255),
    executor_param character varying(4000),
    executor_timeout integer DEFAULT 0,
    trigger_id integer DEFAULT 0 NOT NULL,
    trigger_time timestamp without time zone,
    trigger_code character varying(255) DEFAULT '0'::character varying NOT NULL,
    trigger_msg character varying(2048),
    handle_time timestamp without time zone,
    handle_code integer DEFAULT 0 NOT NULL,
    handle_msg character varying(2048),
    runresult character varying(4000)
);

create index ind_fs_trigger_log on public.fs_trigger_log(job_id);
create index ind_fs_trigger_id on public.fs_trigger_log(trigger_id);

--
-- Name: fs_trigger_logglue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_trigger_logglue (
    id integer NOT NULL,
    job_id integer NOT NULL,
    glue_type character varying(50),
    glue_source text,
    glue_remark character varying(128) NOT NULL,
    add_time timestamp without time zone,
    update_time timestamp without time zone
);



--
-- Name: fs_trigger_registry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_trigger_registry (
    id integer NOT NULL,
    registry_group character varying(255) NOT NULL,
    registry_key character varying(255) NOT NULL,
    registry_value character varying(255) NOT NULL,
    update_time timestamp without time zone DEFAULT LOCALTIMESTAMP NOT NULL,
    registry_type character varying(10)
);



--
-- Name: COLUMN fs_trigger_registry.registry_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fs_trigger_registry.registry_type IS 'executor 注册类型 ''''(自动)/''manual''(手动)';


--
-- Name: fs_trigger_task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_trigger_task (
    id integer NOT NULL,
    taskid integer NOT NULL,
    trigger_time timestamp without time zone,
    handle_time timestamp without time zone,
    handle_code integer DEFAULT 0 NOT NULL
);



--
-- Name: fs_triggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fs_triggers (
    sched_name character varying(120) NOT NULL,
    trigger_name character varying(200) NOT NULL,
    trigger_group character varying(200) NOT NULL,
    job_name character varying(200) NOT NULL,
    job_group character varying(200) NOT NULL,
    description character varying(250),
    next_fire_time bigint,
    prev_fire_time bigint,
    priority integer,
    trigger_state character varying(16) NOT NULL,
    trigger_type character varying(8) NOT NULL,
    start_time bigint NOT NULL,
    end_time bigint,
    calendar_name character varying(200),
    misfire_instr smallint,
    job_data bytea
);



--
-- Name: s_fs_dfc_tasks; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_dfc_tasks
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_job_handler; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_job_handler
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_group; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_group
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_info; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_info
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_log; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_log
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_logglue; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_logglue
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_registry; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_registry
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: s_fs_trigger_task; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.s_fs_trigger_task
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Data for Name: fs_blob_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_blob_triggers (sched_name, trigger_name, trigger_group, blob_data) FROM stdin;
\.


--
-- Data for Name: fs_calendars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_calendars (sched_name, calendar_name, calendar) FROM stdin;
\.


--
-- Data for Name: fs_cron_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_cron_triggers (sched_name, trigger_name, trigger_group, cron_expression, time_zone_id) FROM stdin;
quartzScheduler	500	system	0 0 0 * * ? 	Asia/Shanghai
\.


--
-- Data for Name: fs_dfc_job_handler; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_dfc_job_handler (id, executorid, handlername, injecttype, strategy, strategyparam) FROM stdin;
\.


--
-- Data for Name: fs_dfc_job_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_dfc_job_info (id, job_group, job_cron, job_desc, add_time, update_time, author, alarm_email, executor_route_strategy, executor_handler, executor_param, executor_block_strategy, executor_fail_strategy, executor_timeout, glue_type, glue_source, glue_remark, glue_updatetime, child_jobkey, resulttype, depend_job_result, taskid, job_order_in_task, job_name) FROM stdin;
500	1001	\N	do clean 	2018-07-11 14:00:33.153668	2018-07-11 14:00:33.153668		\N	SHARDING_BROADCAST	cleanExecutorLocalLog	{"bulk":false,"obs":[{"period":"1","timeUnit":"WEEK"}],"type":"param"}	DISCARD_LATER	FAIL_ALARM	0	BEAN	\N	\N	2018-07-11 14:00:33.153668		param	[]	500	1	clean executor log file
\.


--
-- Data for Name: fs_dfc_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_dfc_tasks (id, author, task_name, task_uuid, user_identity, listener_name, task_cron, description, remark, task_level) FROM stdin;
500	admin	system clean log task.	bf6b4787-4515-4555-8cd2-9c0517f534cc			0 0 0 * * ? 	Clean log files daily	\N	system
\.


--
-- Data for Name: fs_fired_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_fired_triggers (sched_name, entry_id, trigger_name, trigger_group, instance_name, fired_time, sched_time, priority, state, job_name, job_group, is_nonconcurrent, requests_recovery) FROM stdin;
\.


--
-- Data for Name: fs_job_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_job_details (sched_name, job_name, job_group, description, job_class_name, is_durable, is_nonconcurrent, is_update_data, requests_recovery, job_data) FROM stdin;
quartzScheduler	500	system	\N	com.rt.job.admin.core.jobbean.JobLogCleanBean	f	f	f	f	\\xaced0005737200156f72672e71756172747a2e4a6f62446174614d61709fb083e8bfa9b0cb020000787200266f72672e71756172747a2e7574696c732e537472696e674b65794469727479466c61674d61708208e8c3fbc55d280200015a0013616c6c6f77735472616e7369656e74446174617872001d6f72672e71756172747a2e7574696c732e4469727479466c61674d617013e62ead28760ace0200025a000564697274794c00036d617074000f4c6a6176612f7574696c2f4d61703b787000737200116a6176612e7574696c2e486173684d61700507dac1c31660d103000246000a6c6f6164466163746f724900097468726573686f6c6478703f40000000000010770800000010000000007800
\.


--
-- Data for Name: fs_locks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_locks (sched_name, lock_name) FROM stdin;
quartzScheduler	TRIGGER_ACCESS
quartzScheduler	STATE_ACCESS
\.


--
-- Data for Name: fs_paused_trigger_grps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_paused_trigger_grps (sched_name, trigger_group) FROM stdin;
\.


--
-- Data for Name: fs_scheduler_state; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_scheduler_state (sched_name, instance_name, last_checkin_time, checkin_interval) FROM stdin;
quartzScheduler	node1231536913607890	1536916613411	5000
\.


--
-- Data for Name: fs_simple_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_simple_triggers (sched_name, trigger_name, trigger_group, repeat_count, repeat_interval, times_triggered) FROM stdin;
\.


--
-- Data for Name: fs_simprop_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_simprop_triggers (sched_name, trigger_name, trigger_group, str_prop_1, str_prop_2, str_prop_3, int_prop_1, int_prop_2, long_prop_1, long_prop_2, dec_prop_1, dec_prop_2, bool_prop_1, bool_prop_2) FROM stdin;
\.


--
-- Data for Name: fs_trigger_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_trigger_group (id, app_name, title, group_order, address_type, address_list) FROM stdin;
1000	rt-job-executor	commonExecutor	1	0	127.0.0.1:9090
1001	rt-job-executor	returnOPSExecutor	2	0	127.0.0.1:9090
\.


--
-- Data for Name: fs_trigger_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_trigger_log (id, job_group, job_id, glue_type, log_locate, executor_address, executor_handler, executor_param, executor_timeout, trigger_id, trigger_time, trigger_code, trigger_msg, handle_time, handle_code, handle_msg, runresult) FROM stdin;
\.


--
-- Data for Name: fs_trigger_logglue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_trigger_logglue (id, job_id, glue_type, glue_source, glue_remark, add_time, update_time) FROM stdin;
\.


--
-- Data for Name: fs_trigger_registry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_trigger_registry (id, registry_group, registry_key, registry_value, update_time, registry_type) FROM stdin;
1001	EXECUTOR	rt-job-executor	127.0.0.1:9090	2018-09-14 17:16:49.093914	\N
\.


--
-- Data for Name: fs_trigger_task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_trigger_task (id, taskid, trigger_time, handle_time, handle_code) FROM stdin;
1284	500	2018-09-14 00:00:01.315	2018-09-14 00:00:02.567	200
\.


--
-- Data for Name: fs_triggers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fs_triggers (sched_name, trigger_name, trigger_group, job_name, job_group, description, next_fire_time, prev_fire_time, priority, trigger_state, trigger_type, start_time, end_time, calendar_name, misfire_instr, job_data) FROM stdin;
quartzScheduler	500	system	500	system	\N	1536940800000	1536854400000	5	WAITING	CRON	1536828201000	0	\N	2	\\x
\.


--
-- Name: s_fs_dfc_tasks; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_dfc_tasks', 1163, true);


--
-- Name: s_fs_job_handler; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_job_handler', 1000, false);


--
-- Name: s_fs_trigger_group; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_group', 1001, true);


--
-- Name: s_fs_trigger_info; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_info', 1163, true);


--
-- Name: s_fs_trigger_log; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_log', 2139, true);


--
-- Name: s_fs_trigger_logglue; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_logglue', 1000, false);


--
-- Name: s_fs_trigger_registry; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_registry', 1001, true);


--
-- Name: s_fs_trigger_task; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.s_fs_trigger_task', 2130, true);


--
-- Name: fs_blob_triggers fs_blob_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_blob_triggers
    ADD CONSTRAINT fs_blob_triggers_pkey PRIMARY KEY (sched_name, trigger_name, trigger_group);


--
-- Name: fs_calendars fs_calendars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_calendars
    ADD CONSTRAINT fs_calendars_pkey PRIMARY KEY (sched_name, calendar_name);


--
-- Name: fs_cron_triggers fs_cron_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_cron_triggers
    ADD CONSTRAINT fs_cron_triggers_pkey PRIMARY KEY (sched_name, trigger_name, trigger_group);


--
-- Name: fs_dfc_job_handler fs_dfc_job_handler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_dfc_job_handler
    ADD CONSTRAINT fs_dfc_job_handler_pkey PRIMARY KEY (id);


--
-- Name: fs_dfc_job_info fs_dfc_job_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_dfc_job_info
    ADD CONSTRAINT fs_dfc_job_info_pkey PRIMARY KEY (id);


--
-- Name: fs_dfc_tasks fs_dfc_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_dfc_tasks
    ADD CONSTRAINT fs_dfc_tasks_pkey PRIMARY KEY (id);


--
-- Name: fs_fired_triggers fs_fired_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_fired_triggers
    ADD CONSTRAINT fs_fired_triggers_pkey PRIMARY KEY (sched_name, entry_id);


--
-- Name: fs_job_details fs_job_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_job_details
    ADD CONSTRAINT fs_job_details_pkey PRIMARY KEY (sched_name, job_name, job_group);


--
-- Name: fs_locks fs_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_locks
    ADD CONSTRAINT fs_locks_pkey PRIMARY KEY (sched_name, lock_name);


--
-- Name: fs_paused_trigger_grps fs_paused_trigger_grps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_paused_trigger_grps
    ADD CONSTRAINT fs_paused_trigger_grps_pkey PRIMARY KEY (sched_name, trigger_group);


--
-- Name: fs_scheduler_state fs_scheduler_state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_scheduler_state
    ADD CONSTRAINT fs_scheduler_state_pkey PRIMARY KEY (sched_name, instance_name);


--
-- Name: fs_simple_triggers fs_simple_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_simple_triggers
    ADD CONSTRAINT fs_simple_triggers_pkey PRIMARY KEY (sched_name, trigger_name, trigger_group);


--
-- Name: fs_simprop_triggers fs_simprop_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_simprop_triggers
    ADD CONSTRAINT fs_simprop_triggers_pkey PRIMARY KEY (sched_name, trigger_name, trigger_group);


--
-- Name: fs_trigger_group fs_trigger_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_group
    ADD CONSTRAINT fs_trigger_group_pkey PRIMARY KEY (id);


--
-- Name: fs_trigger_group fs_trigger_group_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_group
    ADD CONSTRAINT fs_trigger_group_title_key UNIQUE (title);


--
-- Name: fs_trigger_log fs_trigger_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_log
    ADD CONSTRAINT fs_trigger_log_pkey PRIMARY KEY (id);


--
-- Name: fs_trigger_logglue fs_trigger_logglue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_logglue
    ADD CONSTRAINT fs_trigger_logglue_pkey PRIMARY KEY (id);


--
-- Name: fs_trigger_registry fs_trigger_registry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_registry
    ADD CONSTRAINT fs_trigger_registry_pkey PRIMARY KEY (id);


--
-- Name: fs_trigger_task fs_trigger_task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_task
    ADD CONSTRAINT fs_trigger_task_pkey PRIMARY KEY (id);


--
-- Name: fs_triggers fs_triggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_triggers
    ADD CONSTRAINT fs_triggers_pkey PRIMARY KEY (sched_name, trigger_name, trigger_group);


--
-- Name: fs_dfc_job_info_taskid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fs_dfc_job_info_taskid ON public.fs_dfc_job_info USING btree (taskid);


--
-- Name: fs_dfc_tasks_task_uuid_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fs_dfc_tasks_task_uuid_uindex ON public.fs_dfc_tasks USING btree (task_uuid);


--
-- Name: idx_fs_ft_inst_job_req_rcvry; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_inst_job_req_rcvry ON public.fs_fired_triggers USING btree (sched_name, instance_name, requests_recovery);


--
-- Name: idx_fs_ft_j_g; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_j_g ON public.fs_fired_triggers USING btree (sched_name, job_name, job_group);


--
-- Name: idx_fs_ft_jg; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_jg ON public.fs_fired_triggers USING btree (sched_name, job_group);


--
-- Name: idx_fs_ft_t_g; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_t_g ON public.fs_fired_triggers USING btree (sched_name, trigger_name, trigger_group);


--
-- Name: idx_fs_ft_tg; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_tg ON public.fs_fired_triggers USING btree (sched_name, trigger_group);


--
-- Name: idx_fs_ft_trig_inst_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_ft_trig_inst_name ON public.fs_fired_triggers USING btree (sched_name, instance_name);


--
-- Name: idx_fs_j_grp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_j_grp ON public.fs_job_details USING btree (sched_name, job_group);


--
-- Name: idx_fs_j_req_recovery; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_j_req_recovery ON public.fs_job_details USING btree (sched_name, requests_recovery);


--
-- Name: idx_fs_t_c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_c ON public.fs_triggers USING btree (sched_name, calendar_name);


--
-- Name: idx_fs_t_g; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_g ON public.fs_triggers USING btree (sched_name, trigger_group);


--
-- Name: idx_fs_t_j; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_j ON public.fs_triggers USING btree (sched_name, job_name, job_group);


--
-- Name: idx_fs_t_jg; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_jg ON public.fs_triggers USING btree (sched_name, job_group);


--
-- Name: idx_fs_t_n_g_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_n_g_state ON public.fs_triggers USING btree (sched_name, trigger_group, trigger_state);


--
-- Name: idx_fs_t_n_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_n_state ON public.fs_triggers USING btree (sched_name, trigger_name, trigger_group, trigger_state);


--
-- Name: idx_fs_t_next_fire_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_next_fire_time ON public.fs_triggers USING btree (sched_name, next_fire_time);


--
-- Name: idx_fs_t_nft_misfire; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_nft_misfire ON public.fs_triggers USING btree (sched_name, misfire_instr, next_fire_time);


--
-- Name: idx_fs_t_nft_st; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_nft_st ON public.fs_triggers USING btree (sched_name, trigger_state, next_fire_time);


--
-- Name: idx_fs_t_nft_st_misfire; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_nft_st_misfire ON public.fs_triggers USING btree (sched_name, misfire_instr, next_fire_time, trigger_state);


--
-- Name: idx_fs_t_nft_st_misfire_grp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_nft_st_misfire_grp ON public.fs_triggers USING btree (sched_name, misfire_instr, next_fire_time, trigger_group, trigger_state);


--
-- Name: idx_fs_t_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fs_t_state ON public.fs_triggers USING btree (sched_name, trigger_state);


--
-- Name: fs_dfc_job_handler tib_fs_job_handler; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tib_fs_job_handler BEFORE INSERT ON public.fs_dfc_job_handler FOR EACH ROW EXECUTE PROCEDURE public.trigger_fct_tib_fs_job_handler();


--
-- Name: fs_trigger_registry tib_fs_trigger_registry; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tib_fs_trigger_registry BEFORE INSERT ON public.fs_trigger_registry FOR EACH ROW EXECUTE PROCEDURE public.trigger_fct_tib_fs_trigger_registry();


--
-- Name: fs_blob_triggers fs_blob_triggers_sched_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_blob_triggers
    ADD CONSTRAINT fs_blob_triggers_sched_name_fkey FOREIGN KEY (sched_name, trigger_name, trigger_group) REFERENCES public.fs_triggers(sched_name, trigger_name, trigger_group);


--
-- Name: fs_cron_triggers fs_cron_triggers_sched_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_cron_triggers
    ADD CONSTRAINT fs_cron_triggers_sched_name_fkey FOREIGN KEY (sched_name, trigger_name, trigger_group) REFERENCES public.fs_triggers(sched_name, trigger_name, trigger_group);


--
-- Name: fs_dfc_job_info fs_dfc_job_tasks_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_dfc_job_info
    ADD CONSTRAINT fs_dfc_job_tasks_id_fk FOREIGN KEY (taskid) REFERENCES public.fs_dfc_tasks(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fs_simple_triggers fs_simple_triggers_sched_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_simple_triggers
    ADD CONSTRAINT fs_simple_triggers_sched_name_fkey FOREIGN KEY (sched_name, trigger_name, trigger_group) REFERENCES public.fs_triggers(sched_name, trigger_name, trigger_group);


--
-- Name: fs_simprop_triggers fs_simprop_triggers_sched_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_simprop_triggers
    ADD CONSTRAINT fs_simprop_triggers_sched_name_fkey FOREIGN KEY (sched_name, trigger_name, trigger_group) REFERENCES public.fs_triggers(sched_name, trigger_name, trigger_group);


--
-- Name: fs_trigger_task fs_trigger_task_taskid_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_trigger_task
    ADD CONSTRAINT fs_trigger_task_taskid_fk FOREIGN KEY (taskid) REFERENCES public.fs_dfc_tasks(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: fs_triggers fs_triggers_sched_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fs_triggers
    ADD CONSTRAINT fs_triggers_sched_name_fkey FOREIGN KEY (sched_name, job_name, job_group) REFERENCES public.fs_job_details(sched_name, job_name, job_group);


CREATE OR REPLACE FUNCTION trigger_delete_fs_trigger_task()
RETURNS TRIGGER AS $$
BEGIN
    -- 删除 fs_other_table 表中与 trigger_id 相关的记录
    DELETE FROM "public"."fs_trigger_task"
    WHERE "id" = OLD."trigger_id";

    -- 返回已删除的记录
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_delete_fs_trigger_task
AFTER DELETE ON "public"."fs_trigger_log"
FOR EACH ROW
EXECUTE PROCEDURE trigger_delete_fs_trigger_task();

--
-- PostgreSQL database dump complete
--



