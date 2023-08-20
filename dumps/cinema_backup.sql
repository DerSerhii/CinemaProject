--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-08-19 19:39:58 EEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 16415)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO cinemauser;

--
-- TOC entry 215 (class 1259 OID 16414)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO cinemauser;

--
-- TOC entry 3547 (class 0 OID 0)
-- Dependencies: 215
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- TOC entry 218 (class 1259 OID 16424)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO cinemauser;

--
-- TOC entry 217 (class 1259 OID 16423)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO cinemauser;

--
-- TOC entry 3548 (class 0 OID 0)
-- Dependencies: 217
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- TOC entry 214 (class 1259 OID 16408)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO cinemauser;

--
-- TOC entry 213 (class 1259 OID 16407)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO cinemauser;

--
-- TOC entry 3549 (class 0 OID 0)
-- Dependencies: 213
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- TOC entry 227 (class 1259 OID 16532)
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO cinemauser;

--
-- TOC entry 229 (class 1259 OID 16546)
-- Name: cinema_film; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_film (
    id bigint NOT NULL,
    name character varying(130) NOT NULL,
    description text NOT NULL,
    starring character varying(200) NOT NULL,
    director character varying(50) NOT NULL,
    duration interval NOT NULL,
    poster character varying(100),
    to_rental boolean NOT NULL
);


ALTER TABLE public.cinema_film OWNER TO cinemauser;

--
-- TOC entry 228 (class 1259 OID 16545)
-- Name: cinema_film_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_film_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_film_id_seq OWNER TO cinemauser;

--
-- TOC entry 3550 (class 0 OID 0)
-- Dependencies: 228
-- Name: cinema_film_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_film_id_seq OWNED BY public.cinema_film.id;


--
-- TOC entry 231 (class 1259 OID 16555)
-- Name: cinema_screencinema; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_screencinema (
    id bigint NOT NULL,
    name character varying(20) NOT NULL,
    capacity smallint NOT NULL,
    CONSTRAINT cinema_screencinema_capacity_check CHECK ((capacity >= 0))
);


ALTER TABLE public.cinema_screencinema OWNER TO cinemauser;

--
-- TOC entry 230 (class 1259 OID 16554)
-- Name: cinema_screencinema_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_screencinema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_screencinema_id_seq OWNER TO cinemauser;

--
-- TOC entry 3551 (class 0 OID 0)
-- Dependencies: 230
-- Name: cinema_screencinema_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_screencinema_id_seq OWNED BY public.cinema_screencinema.id;


--
-- TOC entry 233 (class 1259 OID 16573)
-- Name: cinema_showtime; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_showtime (
    id bigint NOT NULL,
    price numeric(5,2) NOT NULL,
    film_id bigint NOT NULL,
    screen_id bigint NOT NULL,
    attendance smallint NOT NULL,
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    CONSTRAINT cinema_showtime_attendance_check CHECK ((attendance >= 0))
);


ALTER TABLE public.cinema_showtime OWNER TO cinemauser;

--
-- TOC entry 232 (class 1259 OID 16572)
-- Name: cinema_showtime_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_showtime_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_showtime_id_seq OWNER TO cinemauser;

--
-- TOC entry 3552 (class 0 OID 0)
-- Dependencies: 232
-- Name: cinema_showtime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_showtime_id_seq OWNED BY public.cinema_showtime.id;


--
-- TOC entry 220 (class 1259 OID 16457)
-- Name: cinema_spectator; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_spectator (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    wallet numeric(6,2) NOT NULL
);


ALTER TABLE public.cinema_spectator OWNER TO cinemauser;

--
-- TOC entry 222 (class 1259 OID 16468)
-- Name: cinema_spectator_groups; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_spectator_groups (
    id bigint NOT NULL,
    spectator_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.cinema_spectator_groups OWNER TO cinemauser;

--
-- TOC entry 221 (class 1259 OID 16467)
-- Name: cinema_spectator_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_spectator_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_spectator_groups_id_seq OWNER TO cinemauser;

--
-- TOC entry 3553 (class 0 OID 0)
-- Dependencies: 221
-- Name: cinema_spectator_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_spectator_groups_id_seq OWNED BY public.cinema_spectator_groups.id;


--
-- TOC entry 219 (class 1259 OID 16456)
-- Name: cinema_spectator_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_spectator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_spectator_id_seq OWNER TO cinemauser;

--
-- TOC entry 3554 (class 0 OID 0)
-- Dependencies: 219
-- Name: cinema_spectator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_spectator_id_seq OWNED BY public.cinema_spectator.id;


--
-- TOC entry 224 (class 1259 OID 16475)
-- Name: cinema_spectator_user_permissions; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_spectator_user_permissions (
    id bigint NOT NULL,
    spectator_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.cinema_spectator_user_permissions OWNER TO cinemauser;

--
-- TOC entry 223 (class 1259 OID 16474)
-- Name: cinema_spectator_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_spectator_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_spectator_user_permissions_id_seq OWNER TO cinemauser;

--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 223
-- Name: cinema_spectator_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_spectator_user_permissions_id_seq OWNED BY public.cinema_spectator_user_permissions.id;


--
-- TOC entry 235 (class 1259 OID 16596)
-- Name: cinema_ticket; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.cinema_ticket (
    id bigint NOT NULL,
    quantity smallint NOT NULL,
    time_purchase timestamp with time zone NOT NULL,
    showtime_id bigint NOT NULL,
    spectator_id bigint NOT NULL,
    CONSTRAINT cinema_ticket_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.cinema_ticket OWNER TO cinemauser;

--
-- TOC entry 234 (class 1259 OID 16595)
-- Name: cinema_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.cinema_ticket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cinema_ticket_id_seq OWNER TO cinemauser;

--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 234
-- Name: cinema_ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.cinema_ticket_id_seq OWNED BY public.cinema_ticket.id;


--
-- TOC entry 226 (class 1259 OID 16511)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO cinemauser;

--
-- TOC entry 225 (class 1259 OID 16510)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO cinemauser;

--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 225
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- TOC entry 212 (class 1259 OID 16399)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO cinemauser;

--
-- TOC entry 211 (class 1259 OID 16398)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO cinemauser;

--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 211
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- TOC entry 210 (class 1259 OID 16390)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO cinemauser;

--
-- TOC entry 209 (class 1259 OID 16389)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: cinemauser
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO cinemauser;

--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 209
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cinemauser
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- TOC entry 236 (class 1259 OID 16617)
-- Name: django_session; Type: TABLE; Schema: public; Owner: cinemauser
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO cinemauser;

--
-- TOC entry 3278 (class 2604 OID 17466)
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- TOC entry 3279 (class 2604 OID 17467)
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 3277 (class 2604 OID 17468)
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- TOC entry 3285 (class 2604 OID 17469)
-- Name: cinema_film id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_film ALTER COLUMN id SET DEFAULT nextval('public.cinema_film_id_seq'::regclass);


--
-- TOC entry 3286 (class 2604 OID 17470)
-- Name: cinema_screencinema id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_screencinema ALTER COLUMN id SET DEFAULT nextval('public.cinema_screencinema_id_seq'::regclass);


--
-- TOC entry 3288 (class 2604 OID 17471)
-- Name: cinema_showtime id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_showtime ALTER COLUMN id SET DEFAULT nextval('public.cinema_showtime_id_seq'::regclass);


--
-- TOC entry 3280 (class 2604 OID 17472)
-- Name: cinema_spectator id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator ALTER COLUMN id SET DEFAULT nextval('public.cinema_spectator_id_seq'::regclass);


--
-- TOC entry 3281 (class 2604 OID 17473)
-- Name: cinema_spectator_groups id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_groups ALTER COLUMN id SET DEFAULT nextval('public.cinema_spectator_groups_id_seq'::regclass);


--
-- TOC entry 3282 (class 2604 OID 17474)
-- Name: cinema_spectator_user_permissions id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.cinema_spectator_user_permissions_id_seq'::regclass);


--
-- TOC entry 3290 (class 2604 OID 17475)
-- Name: cinema_ticket id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_ticket ALTER COLUMN id SET DEFAULT nextval('public.cinema_ticket_id_seq'::regclass);


--
-- TOC entry 3283 (class 2604 OID 17476)
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- TOC entry 3276 (class 2604 OID 17477)
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- TOC entry 3275 (class 2604 OID 17478)
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- TOC entry 3521 (class 0 OID 16415)
-- Dependencies: 216
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3523 (class 0 OID 16424)
-- Dependencies: 218
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3519 (class 0 OID 16408)
-- Dependencies: 214
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add Token', 6, 'add_token');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change Token', 6, 'change_token');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete Token', 6, 'delete_token');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view Token', 6, 'view_token');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add token', 7, 'add_tokenproxy');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change token', 7, 'change_tokenproxy');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete token', 7, 'delete_tokenproxy');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view token', 7, 'view_tokenproxy');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add Spectator', 8, 'add_spectator');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change Spectator', 8, 'change_spectator');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete Spectator', 8, 'delete_spectator');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view Spectator', 8, 'view_spectator');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add Film', 9, 'add_film');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change Film', 9, 'change_film');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete Film', 9, 'delete_film');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view Film', 9, 'view_film');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add Screen', 10, 'add_screencinema');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change Screen', 10, 'change_screencinema');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete Screen', 10, 'delete_screencinema');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view Screen', 10, 'view_screencinema');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add Showtime', 11, 'add_showtime');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change Showtime', 11, 'change_showtime');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete Showtime', 11, 'delete_showtime');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view Showtime', 11, 'view_showtime');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (45, 'Can add Ticket', 12, 'add_ticket');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (46, 'Can change Ticket', 12, 'change_ticket');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (47, 'Can delete Ticket', 12, 'delete_ticket');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (48, 'Can view Ticket', 12, 'view_ticket');


--
-- TOC entry 3532 (class 0 OID 16532)
-- Dependencies: 227
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3534 (class 0 OID 16546)
-- Dependencies: 229
-- Data for Name: cinema_film; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (1, 'Where The Crawdads Sing', 'Where the Crawdads Sing tells the story of Kya, an abandoned girl who raised herself to adulthood in the dangerous marshlands of North Carolina.', 'Daisy Edgar-Jones, Harris Dickinson, David Strathairn', 'Olivia Newman', '02:06:00', 'poster/2022/07/31/Where_the_crawdads_sing.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (3, 'Thor: Love and Thunder', '“Thor: Love and Thunder,” offering long-awaited clues to what’s in store for the God of Thunder. The film finds Thor (Chris Hemsworth) on a journey unlike anything he’s ever faced – a quest for inner peace. But his retirement is interrupted by a galactic killer known as Gorr the God Butcher (Christian Bale), who seeks the extinction of the gods. To combat the threat, Thor enlists the help of King Valkyrie (Tessa Thompson), Korg (Taika Waititi) and ex-girlfriend Jane Foster (Natalie Portman), who – to Thor’s surprise – inexplicably wields his magical hammer, Mjolnir, as the Mighty Thor. Warning | contains a sequence of flashing lights which might affect customers who are susceptible to photosensitive epilepsy.', 'Dave Bautista, Chris Hemsworth, Christian Bale, Karen Gillan, Natalie Portman, Taika Waititi, Chris Pratt, Russell Crowe', 'Taika Waititi', '01:59:00', 'poster/2022/08/03/Thor_Love_and_thunder.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (4, 'The Bad Guys', 'Nobody has ever failed so hard at trying to be good as The Bad Guys. In the new action-comedy from DreamWorks Animation, based on the New York Times best-selling book series, a crackerjack criminal crew of animal outlaws are about to attempt their most challenging con yet—becoming model citizens. Never have there been five friends as infamous as The Bad Guys—dashing pickpocket Mr. Wolf (Academy Award® winner Sam Rockwell, Three Billboards Outside Ebbing, Missouri), seen-it-all safecracker Mr. Snake (Marc Maron, GLOW), chill master-of-disguise Mr. Shark (Craig Robinson, Hot Tub Time Machine franchise), short-fused “muscle” Mr. Piranha (Anthony Ramos, In the Heights) and sharp-tongued expert hacker Ms. Tarantula (Awkwafina, Crazy Rich Asians), aka “Webs.” But when, after years of countless heists and being the world’s most-wanted villains, the gang is finally caught, Mr. Wolf brokers a deal (that he has no intention of keeping) to save them all from prison: The Bad Guys will go good. Under the tutelage of their mentor Professor Marmalade (Richard Ayoade, Paddington 2), an arrogant (but adorable!) guinea pig, The Bad Guys set out to fool the world that they’ve been transformed. Along the way, though, Mr. Wolf begins to suspect that doing good for real may give him what he’s always secretly longed for: acceptance. So when a new villain threatens the city, can Mr. Wolf persuade the rest of the gang to become … The Good Guys? The film co-stars Zazie Beetz (Joker), Lilly Singh (Bad Moms) and Emmy winner Alex Borstein (The Marvelous Mrs. Maisel).', 'Zazie Beetz, Marc Maron, Richard Ayoade, Lilly Singh, Alex Borstein, Awkwafina , Sam Rockwell, Craig Robinson, Anthony Ramos', 'Pierre Perifel', '01:40:00', 'poster/2022/08/03/The_bad_guys.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (5, 'Top Gun: Maverick', 'After more than thirty years of service as one of the Navy’s top aviators, Pete “Maverick” Mitchell (Tom Cruise) is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him. When he finds himself training a detachment of Top Gun graduates for a specialized mission the likes of which no living pilot has ever seen, Maverick encounters Lt. Bradley Bradshaw (Miles Teller), call sign: “Rooster,” the son of Maverick’s late friend and Radar Intercept Officer Lt. Nick Bradshaw, aka “Goose”. Facing an uncertain future and confronting the ghosts of his past, Maverick is drawn into a confrontation with his own deepest fears, culminating in a mission that demands the ultimate sacrifice from those who will be chosen to fly it.', 'Jon Hamm, Lewis Pullman, Miles Teller, Tom Cruise, Ed Harris, Jennifer Connelly, Glen Powell, Charles Parnell, Danny Ramirez, Jay Ellis, Bashir Salahuddin, Monica Barbaro, Greg Tarzan Davis, Val Kilme', 'Joseph Kosinski', '02:11:00', 'poster/2022/08/03/Top_Gun_Maverick.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (6, 'The Railway Children Return', 'Inspired by one of the most beloved British family films of all time, The Railway Children Return is an enchanting, moving and heart-warming adventure for a new generation. 1944 – As life in Britain’s cities becomes increasingly perilous, three evacuee children – Lily, Pattie and Ted Watts – are sent by their mother from Salford to the Yorkshire village of Oakworth. There to meet them on the train station platform are Bobbie Waterbury (Jenny Agutter, reprising her iconic role in the original film), her daughter, Annie and grandson Thomas, and with their help the evacuees are soon settling into their new life in the countryside. When the children discover injured American soldier Abe hiding out in the railyard at Oakworth Station, they are thrust into a dangerous quest to assist their new friend who, like them, is a long way from home.', 'Jenny Agutter, Sheridan Smith, Gabriel Freilich, Joanne James, Tom Courtenay', 'Morgan Matthews', '01:35:00', 'poster/2022/08/05/Theatrical_poster_for_The_Railway_Children_Return.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (7, 'Minions: The Rise of Gru', 'This summer, from the biggest global animated franchise in history, comes the origin story of how the world’s greatest supervillain first met his iconic Minions, forged cinema’s most despicable crew and faced off against the most unstoppable criminal force ever assembled in Minions: The Rise of Gru.', 'Lucy Lawless, Dolph Lundgren, Alan Arkin, Danny Trejo, Taraji P. Henson, Julie Andrews, Russell Brand, Jean-Claude Van Damme, RZA , Michelle Yeoh, Steve Carell', 'Jonathan Del Val, Brad Ableson, Kyle Balda', '01:28:00', 'poster/2022/08/07/MInioms.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (8, 'Elvis', 'From Oscar-nominated visionary filmmaker Baz Luhrmann comes Warner Bros. Pictures’ drama “Elvis,” starring Austin Butler and Oscar winner Tom Hanks. The film explores the life and music of Elvis Presley (Butler), seen through the prism of his complicated relationship with his enigmatic manager, Colonel Tom Parker (Hanks). The story delves into the complex dynamic between Presley and Parker spanning over 20 years, from Presley’s rise to fame to his unprecedented stardom, against the backdrop of the evolving cultural landscape and loss of innocence in America. Central to that journey is one of the most significant and influential people in Elvis’s life, Priscilla Presley (Olivia DeJonge).', 'Austin Butler, Olivia DeJonge, Xavier Samuel, Alton Mason, Tom Hanks, Dacre Montgomery', 'Baz Luhrmann', '02:40:00', 'poster/2022/08/08/Elvis.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (9, 'Nope', '“What’s a bad miracle?” Oscar® winner Jordan Peele disrupted and redefined modern horror with Get Out and then Us. Now, he reimagines the summer movie with a new pop nightmare: the expansive horror epic, Nope. The film reunites Peele with Oscar® winner Daniel Kaluuya (Get Out, Judas and the Black Messiah), who is joined by Keke Palmer (Hustlers, Alice) and Oscar® nominee Steven Yeun (Minari, Okja) as residents in a lonely gulch of inland California who bear witness to an uncanny and chilling discovery. Nope, which co-stars Michael Wincott (Hitchcock, Westworld) and Brandon Perea (The OA, American Insurrection), is written and directed by Jordan Peele and is produced by Ian Cooper (Us, Candyman) and Jordan Peele for Monkeypaw Productions', 'Keke Palmer, Steven Yeun, Michael Wincott, Brandon Perea, Daniel Kaluuya', 'Jordan Peele', '02:10:00', 'poster/2022/08/13/Nope.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (12, 'Dragon Ball Super: Super Hero (Dubbed)', 'The Red Ribbon Army was once destroyed by Son Goku. Individuals, who carry on its spirit, have created the ultimate Androids, Gamma 1 and Gamma 2. These two Androids call themselves “Super Heroes”. They start attacking Piccolo and Gohan... What is the New Red Ribbon Army’s objective? In the face of approaching danger, it is time to awaken, Super Hero!', 'Ryoma Takeuchi, Ryô Horikawa, Miyu Irino, Aya Hirano, Hiroshi Kamiya, Toshio Furukawa, Aya Hisakawa, Masako Nozawa, Mamoru Miyano, Mayumi Tanaka, Yûko Minaguchi, Takeshi Kusao, Volcano Ota', 'Tetsuro Kodama', '02:11:00', 'poster/2022/08/18/Dragon_hNhZ2Za.png', true);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (2, 'Bullet Train', 'Based on the Japanese novel, Maria Beetle by Kotaro Isaka, five assassins find themselves on a fast-moving bullet train from Tokyo to Morioka with only a few stops in between. They discover their missions are not unrelated to one another. The question becomes, who will make it off the train alive and what awaits them at the terminal station?!', 'Aaron Taylor-Johnson, Brad Pitt, Andrew Koji, Hiroyuki Sanada, Joey King, Benito A Martínez Ocasio, Michael Shannon, Brian Tyree Henry', 'David Leitch', '02:06:00', 'poster/2022/08/03/Bullet_train.png', false);
INSERT INTO public.cinema_film (id, name, description, starring, director, duration, poster, to_rental) VALUES (18, 'Test Film 2 + 0.5 = 3 hour', 'Test Film', 'Test Film', 'Test Film', '02:30:00', NULL, true);


--
-- TOC entry 3536 (class 0 OID 16555)
-- Dependencies: 231
-- Data for Name: cinema_screencinema; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.cinema_screencinema (id, name, capacity) VALUES (1, 'green', 80);
INSERT INTO public.cinema_screencinema (id, name, capacity) VALUES (2, 'red', 80);
INSERT INTO public.cinema_screencinema (id, name, capacity) VALUES (3, 'blue', 70);


--
-- TOC entry 3538 (class 0 OID 16573)
-- Dependencies: 233
-- Data for Name: cinema_showtime; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (803, 10.00, 8, 3, 0, '2023-08-16 15:00:00+03', '2023-08-16 17:40:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (804, 10.00, 7, 3, 0, '2023-08-17 16:10:00+03', '2023-08-17 17:38:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (805, 10.00, 4, 3, 0, '2023-08-18 15:30:00+03', '2023-08-18 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (806, 10.00, 4, 3, 0, '2023-08-19 15:30:00+03', '2023-08-19 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (807, 10.00, 4, 3, 0, '2023-08-20 15:30:00+03', '2023-08-20 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (808, 10.00, 4, 3, 0, '2023-08-21 15:30:00+03', '2023-08-21 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (809, 10.00, 4, 3, 0, '2023-08-22 15:30:00+03', '2023-08-22 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (810, 10.00, 4, 3, 0, '2023-08-23 15:30:00+03', '2023-08-23 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (811, 10.00, 4, 3, 0, '2023-08-24 15:30:00+03', '2023-08-24 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (812, 10.00, 4, 3, 0, '2023-08-25 15:30:00+03', '2023-08-25 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (813, 10.00, 4, 3, 0, '2023-08-26 15:30:00+03', '2023-08-26 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (814, 10.00, 4, 3, 0, '2023-08-27 15:30:00+03', '2023-08-27 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (815, 10.00, 4, 3, 0, '2023-08-28 15:30:00+03', '2023-08-28 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (816, 10.00, 4, 3, 0, '2023-08-29 15:30:00+03', '2023-08-29 17:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (817, 10.00, 8, 1, 0, '2023-08-17 18:30:00+03', '2023-08-17 21:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (818, 10.00, 8, 1, 0, '2023-08-18 18:30:00+03', '2023-08-18 21:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (819, 10.00, 8, 2, 0, '2023-08-17 19:30:00+03', '2023-08-17 22:10:00+03');
INSERT INTO public.cinema_showtime (id, price, film_id, screen_id, attendance, start, "end") VALUES (820, 10.00, 7, 1, 0, '2023-08-19 15:30:00+03', '2023-08-19 16:58:00+03');


--
-- TOC entry 3525 (class 0 OID 16457)
-- Dependencies: 220
-- Data for Name: cinema_spectator; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.cinema_spectator (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, wallet) VALUES (15, 'pbkdf2_sha256$320000$QeMfSd9EpCqUd5NgfvvhcM$qvyiwDB4zr5rU2rfUXtTdtf+kOPIpgKcZT1jV1dtaLo=', '2023-08-10 15:05:36.368867+03', true, 'CinemaAdmin', '', '', '', true, true, '2023-07-23 10:03:09.255231+03', 0.00);
INSERT INTO public.cinema_spectator (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, wallet) VALUES (14, 'pbkdf2_sha256$320000$dlh64BMh5ylvTCXQbenSCV$/CrnksNmRV8umC6TOfoI0EWCJ+CGW+UpKBwCG6v1+1c=', '2023-07-09 11:57:40.110477+03', false, 'test', '', '', '', false, true, '2023-07-09 11:57:39.786757+03', 0.00);
INSERT INTO public.cinema_spectator (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, wallet) VALUES (13, 'pbkdf2_sha256$320000$mw02IeO40zEWUcv4UjYA7F$YWmpbOMEktIHAEfYsLVZpN01kJINTpw3NAgaaLSx8fk=', '2023-08-19 15:16:26.275195+03', true, 'admin', '', '', '', true, true, '2023-04-13 14:18:57.202833+03', 0.00);
INSERT INTO public.cinema_spectator (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, wallet) VALUES (1, 'pbkdf2_sha256$320000$vG4cQTB0oojm83tupcwVNk$O4D+BZ4Gu4sLxA5CLwZPeRbYR1izSIubZSkRIMID9tw=', '2023-07-22 09:43:53.418717+03', true, 'SAdmin', '', '', '', true, true, '2022-08-27 10:00:18.279641+03', 0.00);


--
-- TOC entry 3527 (class 0 OID 16468)
-- Dependencies: 222
-- Data for Name: cinema_spectator_groups; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3529 (class 0 OID 16475)
-- Dependencies: 224
-- Data for Name: cinema_spectator_user_permissions; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3540 (class 0 OID 16596)
-- Dependencies: 235
-- Data for Name: cinema_ticket; Type: TABLE DATA; Schema: public; Owner: cinemauser
--



--
-- TOC entry 3531 (class 0 OID 16511)
-- Dependencies: 226
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (1, '2022-07-31 17:30:34.011066+03', '2', 'alinka', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (2, '2022-07-31 17:31:21.579723+03', '2', 'alinka', 2, '[]', 6, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (3, '2022-07-31 17:32:06.355866+03', '1', 'Green', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (4, '2022-07-31 17:40:01.671738+03', '1', 'Where The Crawdads Sing', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (5, '2022-07-31 17:40:39.720108+03', '1', 'Where The Crawdads Sing', 2, '[{"changed": {"fields": ["Duration"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (6, '2022-07-31 17:40:50.508999+03', '1', 'Where The Crawdads Sing', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (7, '2022-07-31 17:42:18.365953+03', '1', 'Showtime 2022-07-31-17:41:43 <Where The Crawdads Sing>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (8, '2022-07-31 18:25:38.791128+03', '3', 'alinka', 1, '[{"added": {}}]', 6, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (9, '2022-07-31 18:26:02.239377+03', '1', 'Showtime 2022-07-31-17:41:43 <Where The Crawdads Sing>', 2, '[]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (10, '2022-08-03 09:47:58.149802+03', '1', 'Showtime 2022-08-03-17:41:43 <Where The Crawdads Sing>', 2, '[{"changed": {"fields": ["Showtime date"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (11, '2022-08-03 09:48:24.775903+03', '2', 'Yellow', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (12, '2022-08-03 09:53:04.048008+03', '2', 'Bullet Train', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (13, '2022-08-03 09:55:39.221592+03', '3', 'Thor: Love and Thunder', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (14, '2022-08-03 09:59:03.276711+03', '4', 'The Bad Guys', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (15, '2022-08-03 10:01:00.750197+03', '5', 'Top Gun: Maverick', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (16, '2022-08-03 10:02:05.56628+03', '1', 'Showtime 2022-08-03-17:00:00 <Where The Crawdads Sing>', 2, '[{"changed": {"fields": ["Showtime start time", "Showtime end time"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (17, '2022-08-03 10:12:57.244562+03', '2', 'Showtime 2022-08-03-10:00:00 <Top Gun: Maverick>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (18, '2022-08-03 10:13:32.163178+03', '3', 'Showtime 2022-08-03-10:00:00 <The Bad Guys>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (19, '2022-08-03 10:13:57.472755+03', '4', 'Showtime 2022-08-03-10:00:00 <Top Gun: Maverick>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (20, '2022-08-03 10:14:56.84181+03', '5', 'Showtime 2022-08-03-14:00:00 <Bullet Train>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (21, '2022-08-03 10:15:23.459675+03', '6', 'Showtime 2022-08-03-16:15:00 <Thor: Love and Thunder>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (22, '2022-08-03 10:21:54.500406+03', '1', 'Showtime 2022-08-04-17:00:00 <Where The Crawdads Sing>', 2, '[{"changed": {"fields": ["Showtime date"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (23, '2022-08-03 10:22:45.95937+03', '3', 'Showtime 2022-08-04-10:00:00 <The Bad Guys>', 2, '[{"changed": {"fields": ["Showtime date"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (24, '2022-08-03 10:23:03.090414+03', '6', 'Showtime 2022-08-04-16:15:00 <Thor: Love and Thunder>', 2, '[{"changed": {"fields": ["Showtime date"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (25, '2022-08-05 09:47:25.006802+03', '3', 'Blue', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (26, '2022-08-05 09:59:37.440582+03', '6', 'The Railway Children Return', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (27, '2022-08-05 10:03:03.56878+03', '9', 'Showtime 2022-08-05-10:00:00 <The Railway Children Return>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (28, '2022-08-05 10:03:39.855217+03', '10', 'Showtime 2022-08-05-10:15:00 <The Railway Children Return>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (29, '2022-08-05 10:04:25.320008+03', '11', 'Showtime 2022-08-05-12:45:00 <The Railway Children Return>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (30, '2022-08-07 11:14:07.669188+03', '7', 'Minions: The Rise of Gru', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (31, '2022-08-07 11:14:47.389296+03', '12', 'Showtime 2022-08-07-11:20:00 <Minions: The Rise of Gru>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (32, '2022-08-07 11:15:30.026012+03', '13', 'Showtime 2022-08-07-15:15:00 <Top Gun: Maverick>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (33, '2022-08-07 11:16:11.78739+03', '14', 'Showtime 2022-08-07-10:00:00 <Bullet Train>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (34, '2022-08-08 10:11:54.832495+03', '8', 'Elvis', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (35, '2022-08-08 10:13:03.484837+03', '15', 'Showtime 2022-08-08-10:15:00 <Elvis>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (36, '2022-08-08 10:13:33.937623+03', '16', 'Showtime 2022-08-08-15:15:00 <Elvis>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (37, '2022-08-08 10:14:04.235823+03', '17', 'Showtime 2022-08-08-18:30:00 <Thor: Love and Thunder>', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (38, '2022-08-13 10:01:10.976741+03', '9', 'Nope', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (39, '2022-08-13 10:02:17.301948+03', '18', '2022-08-13-11:00:00 <Nope>', 1, '[{"added": {}}]', 9, 1);


--
-- TOC entry 3517 (class 0 OID 16399)
-- Dependencies: 212
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.django_content_type (id, app_label, model) VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (6, 'authtoken', 'token');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (7, 'authtoken', 'tokenproxy');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (8, 'cinema', 'spectator');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (9, 'cinema', 'film');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (10, 'cinema', 'screencinema');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (11, 'cinema', 'showtime');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (12, 'cinema', 'ticket');


--
-- TOC entry 3515 (class 0 OID 16390)
-- Dependencies: 210
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2022-08-27 09:55:07.616977+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2022-08-27 09:55:07.646525+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (3, 'auth', '0001_initial', '2022-08-27 09:55:08.141564+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2022-08-27 09:55:08.164109+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (5, 'auth', '0003_alter_user_email_max_length', '2022-08-27 09:55:08.185979+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (6, 'auth', '0004_alter_user_username_opts', '2022-08-27 09:55:08.197257+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (7, 'auth', '0005_alter_user_last_login_null', '2022-08-27 09:55:08.212935+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (8, 'auth', '0006_require_contenttypes_0002', '2022-08-27 09:55:08.22292+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2022-08-27 09:55:08.236853+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (10, 'auth', '0008_alter_user_username_max_length', '2022-08-27 09:55:08.252345+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2022-08-27 09:55:08.260677+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (12, 'auth', '0010_alter_group_name_max_length', '2022-08-27 09:55:08.267854+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (13, 'auth', '0011_update_proxy_permissions', '2022-08-27 09:55:08.278732+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2022-08-27 09:55:08.293119+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (15, 'cinema', '0001_initial', '2022-08-27 09:55:08.817563+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (16, 'admin', '0001_initial', '2022-08-27 09:55:09.025533+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2022-08-27 09:55:09.062036+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2022-08-27 09:55:09.089089+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (19, 'authtoken', '0001_initial', '2022-08-27 09:55:09.233946+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (20, 'authtoken', '0002_auto_20160226_1747', '2022-08-27 09:55:09.315574+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (21, 'authtoken', '0003_tokenproxy', '2022-08-27 09:55:09.325433+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (22, 'cinema', '0002_film_screencinema_alter_spectator_wallet_showtime', '2022-08-27 09:55:09.937533+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (23, 'cinema', '0003_remove_showtime_price_currency_alter_showtime_price_and_more', '2022-08-27 09:55:09.983322+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (24, 'cinema', '0004_alter_spectator_wallet_ticket', '2022-08-27 09:55:10.144186+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (25, 'cinema', '0005_showtime_attendance', '2022-08-27 09:55:10.166955+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (26, 'cinema', '0006_alter_screencinema_name_alter_spectator_is_staff_and_more', '2022-08-27 09:55:10.214932+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (27, 'sessions', '0001_initial', '2022-08-27 09:55:10.394483+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (39, 'cinema', '0007_showtime_end_showtime_start', '2022-09-19 11:14:14.162003+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (40, 'cinema', '0008_alter_showtime_options_remove_showtime_date_and_more', '2022-09-19 13:43:07.572174+03');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (41, 'cinema', '0009_film_to_rental_alter_showtime_attendance_and_more', '2023-08-04 11:17:59.786674+03');


--
-- TOC entry 3541 (class 0 OID 16617)
-- Dependencies: 236
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: cinemauser
--

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('m5zh5gdz9682shu74ynxuqcyte0vfn36', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oRpoc:y3CWY096LWFOcAev5CbTenRj5wFp66rbf8o38a10WqQ', '2022-09-10 10:01:10.728277+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('lzn6y0rck772xy4so06avrdehq4i9nkl', '.eJxVjMsOwiAQRf-FtSHA0KG4dO83kBkeUjU0Ke3K-O_apAvd3nPOfYlA21rD1vMSpiTOQovT78YUH7ntIN2p3WYZ57YuE8tdkQft8jqn_Lwc7t9BpV6_9Vg8DQ4SA7BiNSLggAbJxWwigXXFMTqNniIqAp0KaG8s21gAMybx_gDUYDeh:1oHo8k:dXZfN7CbcwyZHjhZOXTbcNVQHYWWPhpmZOag-52Y2QA', '2022-08-13 18:12:30.589278+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('peoduh48l33io67lchonexecti2qq4vs', '.eJxVjEEOwiAQRe_C2pAODAVduu8ZyDAwUjVtUtqV8e7apAvd_vfef6lI21rj1soSx6wuCtXpd0vEjzLtIN9pus2a52ldxqR3RR-06WHO5Xk93L-DSq1-a5udwR47tl0oxiD0DOisL46JxIsPDCFlYDp3ISNAYhFXgvQYAMWq9wfJuTeh:1oOxjq:nWx2NPSgtNrBWmOQpFTtQ2g5Le-i62_XiVxzhDZqwCs', '2022-09-02 11:52:22.709836+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('ju37vn4zcydpvkoclfdaom8unq228820', '.eJxVjMsOwiAQRf-FtSHA0KG4dO83kBkeUjU0Ke3K-O_apAvd3nPOfYlA21rD1vMSpiTOQovT78YUH7ntIN2p3WYZ57YuE8tdkQft8jqn_Lwc7t9BpV6_9Vg8DQ4SA7BiNSLggAbJxWwigXXFMTqNniIqAp0KaG8s21gAMybx_gDUYDeh:1oJ89n:PBX8VbL0kLJ2bJQ67LSlks-Vrx304vPcDbKoo0YQqUY', '2022-08-17 09:47:03.486503+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('z7eqgamnetwq8x3pyj0koy0kvf3npi71', '.eJxVjMsOwiAQRf-FtSHA0KG4dO83kBkeUjU0Ke3K-O_apAvd3nPOfYlA21rD1vMSpiTOQovT78YUH7ntIN2p3WYZ57YuE8tdkQft8jqn_Lwc7t9BpV6_9Vg8DQ4SA7BiNSLggAbJxWwigXXFMTqNniIqAp0KaG8s21gAMybx_gDUYDeh:1oPKRw:gtmqCGYvx80a0IKFI1NdN_BTWtzruqunHFsyTNI4mFE', '2022-09-03 12:07:24.971692+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('0da4roqw2ku19aqfee1tjm3ar8g87oxm', '.eJxVjEEOwiAQRe_C2pAODAVduu8ZyDAwUjVtUtqV8e7apAvd_vfef6lI21rj1soSx6wuCtXpd0vEjzLtIN9pus2a52ldxqR3RR-06WHO5Xk93L-DSq1-a5udwR47tl0oxiD0DOisL46JxIsPDCFlYDp3ISNAYhFXgvQYAMWq9wfJuTeh:1oKIxw:7BVhyeME_HR6Ckuq8o0ks7eFxg8ahh_EiYr9FVDiRIA', '2022-08-20 15:31:40.680639+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('9otcqdrbruxgf8c4j1opuyf9wojj9cit', '.eJxVjMEOwiAQRP-FsyFAWSgevfcbyMJupWpoUtqT8d9tkx70NMm8N_MWEbe1xK3xEicSV6GVuPyWCfOT60HogfU-yzzXdZmSPBR50iaHmfh1O92_g4Kt7GvHngMpPZrkPLiErG2nDQDiHmMfQGmbFPiQOtDKG28pAzlD2RvuWXy-6U03Og:1oKdIn:VBt5qYf_G8LptgWILz3v2dhoREb331mbOkHAxYKWEGU', '2022-08-21 13:14:33.254179+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('ik8wffsutopsfvo7j7rsjbrrnpos4gj1', '.eJxVjEEOwiAQRe_C2pAODAVduu8ZyDAwUjVtUtqV8e7apAvd_vfef6lI21rj1soSx6wuCtXpd0vEjzLtIN9pus2a52ldxqR3RR-06WHO5Xk93L-DSq1-a5udwR47tl0oxiD0DOisL46JxIsPDCFlYDp3ISNAYhFXgvQYAMWq9wfJuTeh:1oKL9b:y6xxPHo1tHbBUJPMqlv7_fhkeDacI2Sa3KUYnsxznBg', '2022-08-20 17:51:51.147533+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('259jgxu44fl2ihg7hfrxmm4m0cue2m7l', 'e30:1oKbIc:LI4dRnCXAbKJQtj2lDXUiddtdsjfB_KHmSfBXgcqltI', '2022-08-21 11:06:14.327969+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('35bxazjnsb6h17e5bt16ezok880tlfyn', 'e30:1oKbJW:VlOlHKxJrTr8f-oesYFQdprbiBMxgE5Vo5fbYaM6Bts', '2022-08-21 11:07:10.842201+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('yhyn554loc7dewxkh00vbokxausmjn4n', 'e30:1oKbJv:G1e2LcCzpPtDFk69iyZzC8v8eKb3LdVhR4sqHehGEOg', '2022-08-21 11:07:35.027454+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('c1b5bsmm52nxezt41t3td326gq35ownz', '.eJxVjEEOwiAQRe_C2pAODAVduu8ZyDAwUjVtUtqV8e7apAvd_vfef6lI21rj1soSx6wuCtXpd0vEjzLtIN9pus2a52ldxqR3RR-06WHO5Xk93L-DSq1-a5udwR47tl0oxiD0DOisL46JxIsPDCFlYDp3ISNAYhFXgvQYAMWq9wfJuTeh:1oLsru:T9G0QIFmVfwsCjfeGQ6u2jsJKKJSsW8LqePV1XRDQYk', '2022-08-25 00:03:58.87985+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('j9n6rp11ztc5r9c1ch63fvg00xjllnno', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qOfuU:8W645ThBA61a49ydZIBy_YO1EJI2U_2LeKs3syrYA5Q', '2023-08-09 17:54:42.49512+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('zdzpbz2e79pafc44cc875fndjkmo6pdh', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qRen1:Zdvtdsv0xmU7dFiKI5oj14ad_UXVNvaNDmumTleVXls', '2023-08-17 23:19:19.954844+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('izto86my20w3z7cgngbnz7bjmv6j4nbn', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qSEJI:TwmEFMutukaJk30u1GcnFTm_mBtHGrXvXTEnUFEy-w4', '2023-08-19 13:15:00.243318+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('ku91jfq7rsuf7juvye8ciyujlaxswt0u', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oUqbn:FBDnXHV1ZM2GUcOijBLwXWPSiQqDiJcnCzUSVjpwMHw', '2022-09-18 17:28:23.949937+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('ied1qx9692j9f52q7jg645vs0tydw1ri', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oZqwD:7xBfJHhCEhO0cVRVQISGHZOl-R1S4FpEOL8ltoXbxi4', '2022-10-02 12:50:09.372359+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('8hsph03qa19xw61vwk7u20qk4z7b640v', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oZw6r:jPepmyneBoXdbu_ARXJ2TJYpsWRlMvWHouxMVh8cI18', '2022-10-02 18:21:29.522351+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('od222eb52qbvrw33qkrbv6g6ckdzyufn', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oaHUB:gxjXuv14t2RDYWITxA8D3p8HaBV9gL_aUSzBWnjL_Cg', '2022-10-03 17:10:59.027898+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('bo3khpx7fakv20i2cxax0zi3ga6x3cqh', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oaLH2:7G2PxuzEPYyg-sf9ElB2ng8msIe_bg8-H8rsUTknCPM', '2022-10-03 21:13:40.798383+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('ge034unrxhsutnlb3c46ysjfe5uk91r6', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oaLkF:Etuu1Wfb0SWMp3N7P1c_iEFnMs98wQAPQGjjdPgFX14', '2022-10-03 21:43:51.925948+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('yerp1b7u0qvthuoumpjmlko4m7maujck', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oaYGe:O-9SOVkC40mhbik-LsXalX64iqOqjdLXF4S_pglCeTE', '2022-10-04 11:06:08.061387+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('i5wqd43bty8bdrj4zv01tnlupob78hsb', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1oavQK:zRUzGoNXiSKjtNSnb1NEFVkA2Fv60vZsJ6eV-o34fMs', '2022-10-05 11:49:40.856867+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('vd74je8mhiqz43m55wnxarh1727ap1sn', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1obKBL:39enuL08yyqzz0TrErKRcwVA3sXmTMF152y-RSJyXzM', '2022-10-06 14:15:51.878249+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('824k9rj8jdzrtaulgxpxyf1k0q8m8346', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1obebf:eyTgKKLrnSBLodjZcGdddr569HhD3EqLmbaeJWY6xUM', '2022-10-07 12:04:23.252394+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('uv8vm7nyfx5g43aqov40p4jp9828snq3', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1ochzw:fS_gcswD0lCW9yBpfYmNJEIxMqJr3ETHKYOvT2qnms0', '2022-10-10 09:53:48.592666+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('kug35hz83lqgq9vzzxigt1uus5ttcv9f', '.eJxVjMsOwiAQRf-FtSHAyKMu3fcbyMAwUjU0Ke3K-O_apAvd3nPOfYmI21rj1ssSJxIXoUGcfseE-VHaTuiO7TbLPLd1mZLcFXnQLseZyvN6uH8HFXv91konyMorZ5S2dC4GBjaDIc3ecXK5YDAusSWCwt4Cc8BEHhwYZheCeH8A-vQ4Pw:1pmv2o:3IacBfDy-JuevkypxzS0v-Q79-fJIT07LDT19PlvNus', '2023-04-27 14:23:14.560222+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('mxqu9viyuavim5mw7kp8he6m55nf6tgz', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1pmvIh:oVeioJx4ACgX78rMfREgSAszOWPO3KkvU9gnR6sBpk8', '2023-04-27 14:39:39.24544+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('3jcj5r8od5y40l6aov8am4f6uncuxkk2', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qIQWz:P5FYr1GKh3pB1Pbf6x3Gsz5MqvT5i7aguNyRKjD-fQs', '2023-07-23 12:16:37.097442+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('gcypy1cxy35g6hb4ff36uvldzjj4eeg4', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qIt5H:iPBDmMB8rWIhosIHdZPzO_b4vEZZUTbw08_bFO9-ufk', '2023-07-24 18:45:55.795494+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('9icyk9qiou6s4qfnoabvnajqooyhvlr4', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qJ6vJ:dKE4KwYpCjRA_f-gUgRT1DMY6aB2TOL6fImGyXHYLE4', '2023-07-25 09:32:33.137352+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('osokldycqj2dnfxavotp4957jzem1jyb', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qJCwa:ryxDD9okvl2YPAduNwqPVLIybHYZQZX-G_MInJwojoQ', '2023-07-25 15:58:16.147686+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('mnfbb8bieza8401t1iq5iegj5i821x95', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qJWH6:GHFIQZc0RxV3no0rK5s9HHZixNkNu9ygWG7-LWEYTZg', '2023-07-26 12:36:44.561049+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('7q8996xpy49b7uk1oau9giemwtv9gsxm', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qJv5E:YdWeaA11mkRMQzB_KF-fMem4Re34gfIIIbu37gc5ghw', '2023-07-27 15:06:08.42879+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('i98wk6jlp5crbe880ogjvx2xrfylmhq1', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qLfeS:n6QnsyZQy3WT5Wd9GxbrliBvbQLpCFBSySlOXzlIN3w', '2023-08-01 11:01:44.458281+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('kaa014kvz9vb48dr2an7j9u4nxg6dsn7', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qM9Fb:BkmaBtU2vmuZfQ3dJhrOTl3pYoYZgZhkVxz5zemaamk', '2023-08-02 18:38:03.327916+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('h6e3m1fv9v9xbk41klhfjur1pmjxuy56', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qMT93:JUUNX6aPQH46FgQK9uAKVMf4yQV87lPQ3Ea_RZjoMoQ', '2023-08-03 15:52:37.848286+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('wrfxnbusrsrxnoq60yi7n3518tvqym4i', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qMnU3:Sx4C_Y731SYNayG5c-3jodLPLgM4PfWumFxo053wiSE', '2023-08-04 13:35:39.929578+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('jjgweu29vvqs61vdadhmvew0erhacxwq', '.eJxVjMsOwiAQRf-FtSFMebt07zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sTMDdvrdItIjtx2kO7Zb59TbusyR7wo_6ODXnvLzcrh_BxVH_dYTCimjF0Ub7ycAT8opqyEhelsyAqArkE0khdpLi0SRikoJhDNCI3t_ANDMN_U:1qN6LJ:H5Av2bMMQSeshU9vdBYhE_0D3abyVGdSNHOmko2ABW0', '2023-08-05 09:43:53.460933+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('5vzqbdlwc5rvf2mucy95aiq5d2zyv1k2', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qNT8V:SuubXoLmLs5xTcKQT7qsTQeqIub1OAVkD-940WPRb8g', '2023-08-06 10:04:11.155803+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('9it7joz5y56ybfl8qyoc8d388n9lk0zd', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qNsOD:ZzWDRhO2kCXB2mn5mDCUvi1hi2FDl8GZh7ciNk3Pp4Q', '2023-08-07 13:02:05.441564+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('obc2pxtl4ta4byqci4ts30oq05r7eczq', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qOBMv:IWS5b3QjD0CGPFEwYvic5yN2E7CecVAHHl36WCo8YXM', '2023-08-08 09:18:01.895982+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('0bgxl4lupusbaorbj9fvf1bh1csr75x2', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qRnxT:3fnjBcWT40EJJqLxrKbU8JkTbSiv9gt4u7I0JM6hlKs', '2023-08-18 09:06:43.906467+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('7q449213vesq1f5bzbz09t9awos651dm', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qRrcT:eOHPBCjXCQSpn9V3pwbBEty9PyeOdUN0fhws6V4wuMY', '2023-08-18 13:01:17.028382+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('3wqdldpbskm9roolxrqnd11rssj1q72j', '.eJxVjEEOwiAQRe_C2pAylAIu3fcMZJgZpWpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzMk6dfseM9JC6E75jvc2a5rouU9a7og_a9DizPC-H-3dQsJVvHZ2z2TAN0FsCz2EgTx4FDYRr7KgPXWRARpDowAsERPRkTbCGOAb1_gADrjgK:1qU4Q4:0ur2RcTitV8XKkyjgFlUxRvmHpl94opkjaKWuIv2t50', '2023-08-24 15:05:36.402618+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('v1zhs89hqluffhqsvrxpmkqddqy7yr97', '.eJxVjMsOwiAQRf-FtSHAyKMu3fcbyMAwUjU0Ke3K-O_apAvd3nPOfYmI21rj1ssSJxIXoUGcfseE-VHaTuiO7TbLPLd1mZLcFXnQLseZyvN6uH8HFXv91konyMorZ5S2dC4GBjaDIc3ecXK5YDAusSWCwt4Cc8BEHhwYZheCeH8A-vQ4Pw:1qWDf0:IkoK0Yq99lL_1zYsxCxDCnLXKlE3MWj3uOU4uZurni0', '2023-08-30 13:21:54.001455+03');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('3czwyla2hp2j1f8ht4fihr3r0d1teffj', '.eJxVjMsOwiAQRf-FtSHAyKMu3fcbyMAwUjU0Ke3K-O_apAvd3nPOfYmI21rj1ssSJxIXoUGcfseE-VHaTuiO7TbLPLd1mZLcFXnQLseZyvN6uH8HFXv91konyMorZ5S2dC4GBjaDIc3ecXK5YDAusSWCwt4Cc8BEHhwYZheCeH8A-vQ4Pw:1qXKsU:0rok-1CKWPBUx4OdkFwRQMIaRTyqXLFfpto4e15Dqz8', '2023-09-02 15:16:26.284027+03');


--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 215
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 3561 (class 0 OID 0)
-- Dependencies: 217
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 3562 (class 0 OID 0)
-- Dependencies: 213
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 48, true);


--
-- TOC entry 3563 (class 0 OID 0)
-- Dependencies: 228
-- Name: cinema_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_film_id_seq', 18, true);


--
-- TOC entry 3564 (class 0 OID 0)
-- Dependencies: 230
-- Name: cinema_screencinema_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_screencinema_id_seq', 31, true);


--
-- TOC entry 3565 (class 0 OID 0)
-- Dependencies: 232
-- Name: cinema_showtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_showtime_id_seq', 820, true);


--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 221
-- Name: cinema_spectator_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_spectator_groups_id_seq', 1, false);


--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 219
-- Name: cinema_spectator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_spectator_id_seq', 15, true);


--
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 223
-- Name: cinema_spectator_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_spectator_user_permissions_id_seq', 1, false);


--
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 234
-- Name: cinema_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.cinema_ticket_id_seq', 25, true);


--
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 225
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 39, true);


--
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 211
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 12, true);


--
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 209
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cinemauser
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 41, true);


--
-- TOC entry 3305 (class 2606 OID 16454)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 3310 (class 2606 OID 16440)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 3313 (class 2606 OID 16429)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3307 (class 2606 OID 16420)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 16431)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 3302 (class 2606 OID 16413)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3337 (class 2606 OID 16536)
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- TOC entry 3339 (class 2606 OID 16538)
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- TOC entry 3341 (class 2606 OID 16580)
-- Name: cinema_film cinema_film_name_director_21b71add_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_film
    ADD CONSTRAINT cinema_film_name_director_21b71add_uniq UNIQUE (name, director);


--
-- TOC entry 3343 (class 2606 OID 16553)
-- Name: cinema_film cinema_film_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_film
    ADD CONSTRAINT cinema_film_pkey PRIMARY KEY (id);


--
-- TOC entry 3346 (class 2606 OID 16563)
-- Name: cinema_screencinema cinema_screencinema_name_key; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_screencinema
    ADD CONSTRAINT cinema_screencinema_name_key UNIQUE (name);


--
-- TOC entry 3348 (class 2606 OID 16561)
-- Name: cinema_screencinema cinema_screencinema_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_screencinema
    ADD CONSTRAINT cinema_screencinema_pkey PRIMARY KEY (id);


--
-- TOC entry 3351 (class 2606 OID 16578)
-- Name: cinema_showtime cinema_showtime_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_showtime
    ADD CONSTRAINT cinema_showtime_pkey PRIMARY KEY (id);


--
-- TOC entry 3321 (class 2606 OID 16473)
-- Name: cinema_spectator_groups cinema_spectator_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_groups
    ADD CONSTRAINT cinema_spectator_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3324 (class 2606 OID 16483)
-- Name: cinema_spectator_groups cinema_spectator_groups_spectator_id_group_id_091bd6b4_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_groups
    ADD CONSTRAINT cinema_spectator_groups_spectator_id_group_id_091bd6b4_uniq UNIQUE (spectator_id, group_id);


--
-- TOC entry 3315 (class 2606 OID 16464)
-- Name: cinema_spectator cinema_spectator_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator
    ADD CONSTRAINT cinema_spectator_pkey PRIMARY KEY (id);


--
-- TOC entry 3326 (class 2606 OID 16497)
-- Name: cinema_spectator_user_permissions cinema_spectator_user_pe_spectator_id_permission__fb84d059_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_user_permissions
    ADD CONSTRAINT cinema_spectator_user_pe_spectator_id_permission__fb84d059_uniq UNIQUE (spectator_id, permission_id);


--
-- TOC entry 3329 (class 2606 OID 16480)
-- Name: cinema_spectator_user_permissions cinema_spectator_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_user_permissions
    ADD CONSTRAINT cinema_spectator_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3318 (class 2606 OID 16466)
-- Name: cinema_spectator cinema_spectator_username_key; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator
    ADD CONSTRAINT cinema_spectator_username_key UNIQUE (username);


--
-- TOC entry 3354 (class 2606 OID 16602)
-- Name: cinema_ticket cinema_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_ticket
    ADD CONSTRAINT cinema_ticket_pkey PRIMARY KEY (id);


--
-- TOC entry 3333 (class 2606 OID 16519)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3295 (class 2606 OID 16406)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 3297 (class 2606 OID 16404)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3293 (class 2606 OID 16397)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3359 (class 2606 OID 16623)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 3303 (class 1259 OID 16455)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 3308 (class 1259 OID 16451)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 3311 (class 1259 OID 16452)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 3298 (class 1259 OID 16437)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 3335 (class 1259 OID 16544)
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- TOC entry 3344 (class 1259 OID 16581)
-- Name: cinema_screencinema_name_fdc51cd3_like; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_screencinema_name_fdc51cd3_like ON public.cinema_screencinema USING btree (name varchar_pattern_ops);


--
-- TOC entry 3349 (class 1259 OID 16592)
-- Name: cinema_showtime_film_id_3953d62f; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_showtime_film_id_3953d62f ON public.cinema_showtime USING btree (film_id);


--
-- TOC entry 3352 (class 1259 OID 16593)
-- Name: cinema_showtime_screen_id_464c257a; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_showtime_screen_id_464c257a ON public.cinema_showtime USING btree (screen_id);


--
-- TOC entry 3319 (class 1259 OID 16495)
-- Name: cinema_spectator_groups_group_id_cbfb355c; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_spectator_groups_group_id_cbfb355c ON public.cinema_spectator_groups USING btree (group_id);


--
-- TOC entry 3322 (class 1259 OID 16494)
-- Name: cinema_spectator_groups_spectator_id_4d9b7d1b; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_spectator_groups_spectator_id_4d9b7d1b ON public.cinema_spectator_groups USING btree (spectator_id);


--
-- TOC entry 3327 (class 1259 OID 16509)
-- Name: cinema_spectator_user_permissions_permission_id_88788d95; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_spectator_user_permissions_permission_id_88788d95 ON public.cinema_spectator_user_permissions USING btree (permission_id);


--
-- TOC entry 3330 (class 1259 OID 16508)
-- Name: cinema_spectator_user_permissions_spectator_id_55b1a6ce; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_spectator_user_permissions_spectator_id_55b1a6ce ON public.cinema_spectator_user_permissions USING btree (spectator_id);


--
-- TOC entry 3316 (class 1259 OID 16481)
-- Name: cinema_spectator_username_8d0bb7b3_like; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_spectator_username_8d0bb7b3_like ON public.cinema_spectator USING btree (username varchar_pattern_ops);


--
-- TOC entry 3355 (class 1259 OID 16613)
-- Name: cinema_ticket_showtime_id_b5613343; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_ticket_showtime_id_b5613343 ON public.cinema_ticket USING btree (showtime_id);


--
-- TOC entry 3356 (class 1259 OID 16614)
-- Name: cinema_ticket_spectator_id_9d0217e5; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX cinema_ticket_spectator_id_9d0217e5 ON public.cinema_ticket USING btree (spectator_id);


--
-- TOC entry 3331 (class 1259 OID 16530)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 3334 (class 1259 OID 16531)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 3357 (class 1259 OID 16625)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 3360 (class 1259 OID 16624)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: cinemauser
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 3363 (class 2606 OID 16446)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3362 (class 2606 OID 16441)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3361 (class 2606 OID 16432)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3370 (class 2606 OID 16539)
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_cinema_spectator_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_cinema_spectator_id FOREIGN KEY (user_id) REFERENCES public.cinema_spectator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3371 (class 2606 OID 16582)
-- Name: cinema_showtime cinema_showtime_film_id_3953d62f_fk_cinema_film_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_showtime
    ADD CONSTRAINT cinema_showtime_film_id_3953d62f_fk_cinema_film_id FOREIGN KEY (film_id) REFERENCES public.cinema_film(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3372 (class 2606 OID 16587)
-- Name: cinema_showtime cinema_showtime_screen_id_464c257a_fk_cinema_screencinema_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_showtime
    ADD CONSTRAINT cinema_showtime_screen_id_464c257a_fk_cinema_screencinema_id FOREIGN KEY (screen_id) REFERENCES public.cinema_screencinema(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3364 (class 2606 OID 16484)
-- Name: cinema_spectator_groups cinema_spectator_gro_spectator_id_4d9b7d1b_fk_cinema_sp; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_groups
    ADD CONSTRAINT cinema_spectator_gro_spectator_id_4d9b7d1b_fk_cinema_sp FOREIGN KEY (spectator_id) REFERENCES public.cinema_spectator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3365 (class 2606 OID 16489)
-- Name: cinema_spectator_groups cinema_spectator_groups_group_id_cbfb355c_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_groups
    ADD CONSTRAINT cinema_spectator_groups_group_id_cbfb355c_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3367 (class 2606 OID 16503)
-- Name: cinema_spectator_user_permissions cinema_spectator_use_permission_id_88788d95_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_user_permissions
    ADD CONSTRAINT cinema_spectator_use_permission_id_88788d95_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3366 (class 2606 OID 16498)
-- Name: cinema_spectator_user_permissions cinema_spectator_use_spectator_id_55b1a6ce_fk_cinema_sp; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_spectator_user_permissions
    ADD CONSTRAINT cinema_spectator_use_spectator_id_55b1a6ce_fk_cinema_sp FOREIGN KEY (spectator_id) REFERENCES public.cinema_spectator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3373 (class 2606 OID 16603)
-- Name: cinema_ticket cinema_ticket_showtime_id_b5613343_fk_cinema_showtime_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_ticket
    ADD CONSTRAINT cinema_ticket_showtime_id_b5613343_fk_cinema_showtime_id FOREIGN KEY (showtime_id) REFERENCES public.cinema_showtime(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3374 (class 2606 OID 16608)
-- Name: cinema_ticket cinema_ticket_spectator_id_9d0217e5_fk_cinema_spectator_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.cinema_ticket
    ADD CONSTRAINT cinema_ticket_spectator_id_9d0217e5_fk_cinema_spectator_id FOREIGN KEY (spectator_id) REFERENCES public.cinema_spectator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3368 (class 2606 OID 16520)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3369 (class 2606 OID 16525)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_cinema_spectator_id; Type: FK CONSTRAINT; Schema: public; Owner: cinemauser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_cinema_spectator_id FOREIGN KEY (user_id) REFERENCES public.cinema_spectator(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2023-08-19 19:39:58 EEST

--
-- PostgreSQL database dump complete
--

