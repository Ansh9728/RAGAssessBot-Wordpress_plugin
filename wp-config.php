<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the website, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'RAGAssessBot' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', '' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'xx<ji9Kj3ooU@SQc]zJEfW-M:c@<%?wVR7S=lTzpo;fp~HR><]h~$IQ}A*N4cF46' );
define( 'SECURE_AUTH_KEY',  '/u<o_%ZA@8a*q5GMHCMu<nBreMJC9hi[O}BoD^o.8Z#_4DE,6]7TD=Wqo>xZ|LjO' );
define( 'LOGGED_IN_KEY',    ']F|O8.R^%0va7BQzj9M)t(V%Gn@}=OnfelF{K187&4Mx^m-/%}R#}CVu+Gl>Pn7j' );
define( 'NONCE_KEY',        '.(,xsW$4Q#d6O97RGAAfkD_56~H8J^UD^sz{:A<KL]DLN0{m.cfW)abh%-uty@l5' );
define( 'AUTH_SALT',        ')2&|fl1ei$`Eil=]c;Wtq;IH&;n>[)3JYL %6$?Ai)/;0UrG(9%?OP!q;KPmX-a8' );
define( 'SECURE_AUTH_SALT', 'gf?0e6iW`z?a& ;4f)Zi0/I%4X8o&B=CRumo08O?LB#Q.ZI@JQ61!1 {CW>E{B_e' );
define( 'LOGGED_IN_SALT',   '@zswS ~SH* l{e[>H.dE.KV?gOb&=qMmTT?*F62`JeB)7jR |N&=rRC3;Pp-k$h/' );
define( 'NONCE_SALT',       '&CC]eKhN^).?qz-f*% sC`wqNj&E*D<!iWUUB}^mf~M.f~Z_nH3X=Ps]g><x^dv^' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
