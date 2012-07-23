#include <glib.h>
#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>
#include <math.h>

static const char *p="13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171";

static const char *g="11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568";

static const char *h="3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333";

static GHashTable* root;
typedef struct dato{
	
	mpz_t val;
	unsigned long int x1;


} t_dato;

static void getModularInverse(mpz_t a, mpz_t x, mpz_t p)
{
	mpz_t gcd;
	mpz_init(gcd);

	mpz_t b;
	mpz_init(b);

	mpz_gcdext(gcd, a, b, x, p); //a is the inverse
	mpz_clear(gcd);
	mpz_clear(b);

}

static char*  unsignedLongToString(unsigned long int val)
{
	const int n = snprintf(NULL, 0, "%lu", val);
	char* buf=malloc(n+1);
	snprintf(buf, n+1, "%lu", val);
	return buf;
}

static GHashTable* populateHash(const char *h, const char *g)
{
	unsigned long int exponent;
	unsigned long int maxValue=1L << 20;
	
	GHashTable* myHash = g_hash_table_new(g_str_hash, g_str_equal);

	mpz_t g_mpz;
	mpz_t h_mpz;
	mpz_t p_mpz;

	mpz_init(g_mpz);
	mpz_init(h_mpz);
	mpz_init(p_mpz);

	mpz_set_str(g_mpz,g,10);
	mpz_set_str(h_mpz,h,10);
	mpz_set_str(p_mpz,p,10);
	
	for(exponent=0; exponent <= maxValue; exponent++)
	{
		// h / g^x1
		
		mpz_t gx1_mpz, gx1_mpz_inv, mult, r_to_save;

		mpz_init(gx1_mpz);
		mpz_init(gx1_mpz_inv);
		mpz_init(mult);
		mpz_init(r_to_save);

		mpz_powm_ui(gx1_mpz, g_mpz, exponent, p_mpz); //g^x1
		getModularInverse(gx1_mpz_inv, gx1_mpz, p_mpz);

		mpz_mul(mult, h_mpz, gx1_mpz_inv);
		mpz_mod(r_to_save, mult, p_mpz);

		t_dato* d = malloc(sizeof(t_dato));
		d->x1 = exponent;

		char* r_to_save_string = mpz_get_str(NULL, 10, r_to_save);
		g_hash_table_insert(myHash, (gpointer) r_to_save_string,
				(gpointer) d);

		if ((exponent % 1000) == 0 ){
			char* expString = unsignedLongToString(exponent);	
			printf("exponent= %s\n", expString);
			free(expString);
		}

		mpz_clear(gx1_mpz);
		mpz_clear(gx1_mpz_inv);
		mpz_clear(mult);
		mpz_clear(r_to_save);


	}

	mpz_clear(g_mpz);
	mpz_clear(h_mpz);
	mpz_clear(p_mpz);

	return myHash;

}

int main(int argc, char **argv)
{

	root = populateHash(h, g);

	unsigned long int B = 1 << 20;


	unsigned long int 	exponent = 0;
	mpz_t g_mpz, g_B_mpz, p_mpz;
	mpz_init(g_mpz);
	mpz_init(p_mpz);

	mpz_set_str(g_mpz,g,10);
	mpz_set_str(p_mpz,p,10);

	mpz_init(g_B_mpz);

	mpz_powm_ui(g_B_mpz, g_mpz, B, p_mpz);


	for (exponent=0; exponent <=B ; exponent ++)
	{
		mpz_t t;
		mpz_init(t);
		mpz_powm_ui(t,g_B_mpz, exponent, p_mpz);
		char* t_string = mpz_get_str(NULL, 10, t);
		if (g_hash_table_contains(root, (gconstpointer) t_string))
		{

			t_dato* result = (t_dato*) g_hash_table_lookup(root,
					(gconstpointer) t_string);
			printf("x0=%lu, value=%s, x1=%lu\n", exponent,
					t_string,result->x1);
			mpz_t output, mpz_B;
			mpz_init(output);
			mpz_init(mpz_B);
			mpz_set_ui(mpz_B, B);
			mpz_mul_ui(output, mpz_B,exponent);
			mpz_add_ui(output, output, result->x1);

			char* res = mpz_get_str(NULL, 10, output);
			printf("Found result: %s\n", res);

			break;
		}
		mpz_clear(t);
		free(t_string);

	}


	return 0;
}
