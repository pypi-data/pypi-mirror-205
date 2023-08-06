from preprocessing_text_ben import utils

__version__ = '0.0.1'

def word_counts(x):
	return utils._get_word_counts(x)

def char_counts(x):
	return utils._get_char_counts(x)

def avg_wordlength(x):
	return utils._get_avg_wordlength(x)

def stopwords_count(x):
	return utils._get_stopwords_count(x)

def hashtag_couts(x):
	return utils._get_hashtag_couts(x)

def mention_couts(x):
	return utils._get_mention_couts(x)

def digit_counts(x):
	return utils._get_digit_counts(x)

def uppercase_count(x):
	return utils._get_uppercase_count(x)

def cont_to_exp(x):
	return utils._cont_to_exp(x)

def emails(x):
	return utils._get_emails(x)

def remove_emails(x):
	return utils._remove_emails(x)

def urls(x):
	return utils._get_urls(x)

def remove_urls(x):
	return utils._remove_urls(x)

def remove_rt(x):
	return utils._remove_rt(x)

def remove_special_chars(x):
	return utils._remove_special_chars(x)

def remove_html_tags(x):
	return utils._remove_html_tags(x)

def remove_accented_chars(x):
	return utils._remove_accented_chars(x)

def remove_stopwords(x):
	return utils._remove_stopwords(x)

def make_base(x):
	return utils._make_base(x)

def value_count(df, col):
	return utils._get_value_count(df, col)

def remove_common_words(x, freq, n):
	return utils._remove_common_words(x, freq, n)

def remove_rare_words(x, freq, n):
	return utils._remove_rare_words(x, freq, n)

def spelling_checking(x):
	return utils._spelling_checking(x)




