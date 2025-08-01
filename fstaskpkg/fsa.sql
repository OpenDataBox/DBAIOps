CREATE TABLE fsa_object_info (
target_id INTEGER primary key,
last_fsa_begin TIMESTAMP,
last_fsa_end TIMESTAMP,
last_fsa_is_successed BOOLEAN,
last_collect_time timestamp,
last_collect_has_fsaed boolean);



CREATE TABLE public.oracle_sqlstat (
    record_time timestamp without time zone NOT NULL,
    target_id integer NOT NULL,
    sql_id character varying NOT NULL,
    child_number integer,
    plan_hash_value character varying,
    fetches bigint,
    executions bigint,
    parse_calls bigint,
    disk_reads bigint,
    buffer_gets bigint,
    rows_processed bigint,
    elapsed_time bigint,
    cpu_time bigint,
    type smallint,
    startup_time timestamp without time zone,
    cluster_wait_time bigint,
    first_load_time character varying,
    sql_signature character varying,
    user_id character varying,
    db character varying
);

SELECT create_hypertable('oracle_sqlstat', 'record_time',chunk_time_interval => 86400000000);
CREATE INDEX index_oracle_sqlstat ON public.oracle_sqlstat USING btree (target_id, sql_id, record_time);
CREATE INDEX oracle_sqlstat_plan_hash_value_idx ON public.oracle_sqlstat USING btree (plan_hash_value);


CREATE TABLE public.oracle_sqltext (
    target_id integer,
    record_time timestamp without time zone NOT NULL,
    sql_id character varying,
    sqltext text,
    long_sqltext text
);


SELECT create_hypertable('oracle_sqltext', 'record_time',chunk_time_interval => 86400000000);
CREATE UNIQUE INDEX index_oracle_sqltext ON ONLY public.oracle_sqltext USING btree (target_id, sql_id,record_time);
CREATE or replace FUNCTION public.func_sqltext() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
            IF length(New.sqltext) > 1048500 THEN
                New.long_sqltext = New.sqltext;
                New.sqltext = substring(New.sqltext,1, 524288);
                --RAISE NOTICE '新值:%',New.long_sqltext;
            END IF;
    RETURN new;
END ;
$$;
CREATE TRIGGER trigger_sqltext BEFORE INSERT ON public.oracle_sqltext FOR EACH ROW EXECUTE FUNCTION public.func_sqltext();
CREATE INDEX fts_oracle_sqltext_ind ON ONLY public.oracle_sqltext USING gin (to_tsvector('english'::regconfig, sqltext));

CREATE TABLE public.oracle_sqlplan (
    record_time timestamp without time zone,
    target_id bigint NOT NULL,
    sql_id character varying NOT NULL,
    plan_hash_value character varying NOT NULL,
    full_plan_hash_value character varying,
    child_number bigint NOT NULL,
    create_time timestamp without time zone,
    operation character varying,
    options character varying,
    object_node character varying,
    object_num bigint,
    object_owner character varying,
    object_name character varying,
    object_alias character varying,
    object_type character varying,
    optimizer character varying,
    id bigint NOT NULL,
    parent_id bigint,
    depth bigint,
    "position" bigint,
    search_columns bigint,
    cost bigint,
    cardinality bigint,
    bytes bigint,
    partition_start character varying,
    partition_stop character varying,
    partition_id bigint,
    distribution character varying,
    cpu_cost bigint,
    io_cost bigint,
    temp_space bigint,
    access_predicates character varying,
    filter_predicates character varying,
    projection character varying,
    "time" bigint,
    qblock_name character varying,
    remarks character varying,
    con_id bigint
);

SELECT create_hypertable('oracle_sqlplan', 'record_time',chunk_time_interval => 86400000000);
ALTER TABLE public.oracle_sqlplan
    ADD CONSTRAINT oracle_sqlplan_pkey PRIMARY KEY (target_id, sql_id, plan_hash_value, child_number, id,record_time);

CREATE INDEX ind_time_sqlplan ON ONLY public.oracle_sqlplan USING btree (target_id, sql_id, plan_hash_value);
