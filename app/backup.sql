--
-- PostgreSQL database dump
--

\restrict HN3o4sAy1Na3BuFp13zAYhh7UUnIDyIYUUPvX38aLaCqTU6GzDUXRN35KAKgsQc

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    contact character varying(255),
    phone character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: TABLE customer; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.customer IS '客户';


--
-- Name: COLUMN customer.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customer.id IS '主键ID';


--
-- Name: COLUMN customer.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customer.name IS '客户公司名';


--
-- Name: COLUMN customer.contact; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customer.contact IS '联系方式';


--
-- Name: COLUMN customer.phone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customer.phone IS '手机号';


--
-- Name: COLUMN customer.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.customer.created_at IS '建立日期';


--
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_id_seq OWNER TO postgres;

--
-- Name: customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.id;


--
-- Name: order_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_item (
    id integer NOT NULL,
    order_id integer NOT NULL,
    part_name character varying(255),
    material character varying(255),
    quantity integer DEFAULT 1,
    unit_price numeric(10,2) DEFAULT 0,
    process_req character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.order_item OWNER TO postgres;

--
-- Name: TABLE order_item; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.order_item IS '加工件明细';


--
-- Name: COLUMN order_item.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.id IS '主键ID';


--
-- Name: COLUMN order_item.order_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.order_id IS '订单ID';


--
-- Name: COLUMN order_item.part_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.part_name IS '零件名';


--
-- Name: COLUMN order_item.material; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.material IS '材料';


--
-- Name: COLUMN order_item.quantity; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.quantity IS '数量';


--
-- Name: COLUMN order_item.unit_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.unit_price IS '单价';


--
-- Name: COLUMN order_item.process_req; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.process_req IS '工艺要求';


--
-- Name: COLUMN order_item.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_item.created_at IS '建立日期';


--
-- Name: order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_item_id_seq OWNER TO postgres;

--
-- Name: order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_item_id_seq OWNED BY public.order_item.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    order_no character varying(255) NOT NULL,
    customer_id integer NOT NULL,
    status character varying(255) DEFAULT 'pending'::character varying,
    due_date timestamp without time zone,
    total_amount numeric(12,2) DEFAULT 0,
    remark character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: TABLE orders; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.orders IS '订单';


--
-- Name: COLUMN orders.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.id IS '主键ID';


--
-- Name: COLUMN orders.order_no; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.order_no IS '订单编号';


--
-- Name: COLUMN orders.customer_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.customer_id IS '客户ID';


--
-- Name: COLUMN orders.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.status IS '状态：pending待定/to_production待生产/in_production生产中/finished生产完成/shipped已发货/cancelled已取消';


--
-- Name: COLUMN orders.due_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.due_date IS '交期';


--
-- Name: COLUMN orders.total_amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.total_amount IS '总数';


--
-- Name: COLUMN orders.remark; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.remark IS '备注';


--
-- Name: COLUMN orders.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.created_at IS '建立日期';


--
-- Name: COLUMN orders.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.updated_at IS '最后修改日期';


--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: customer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer ALTER COLUMN id SET DEFAULT nextval('public.customer_id_seq'::regclass);


--
-- Name: order_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item ALTER COLUMN id SET DEFAULT nextval('public.order_item_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customer (id, name, contact, phone, created_at) FROM stdin;
\.


--
-- Data for Name: order_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_item (id, order_id, part_name, material, quantity, unit_price, process_req, created_at) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, order_no, customer_id, status, due_date, total_amount, remark, created_at, updated_at) FROM stdin;
\.


--
-- Name: customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_id_seq', 1, false);


--
-- Name: order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_item_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- Name: order_item order_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT order_item_pkey PRIMARY KEY (id);


--
-- Name: orders orders_order_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_order_no_key UNIQUE (order_no);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict HN3o4sAy1Na3BuFp13zAYhh7UUnIDyIYUUPvX38aLaCqTU6GzDUXRN35KAKgsQc

