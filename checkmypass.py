import hashlib
import sys
import requests


def request_api_data(query_char):
    """get data from site"""
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res



def get_password_leaks_count(hashes, hash_to_check):
    """split the returned hashes and count"""
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if  h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    """create sha1 encoded pass and return get_password_leaks_count"""
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    
    return get_password_leaks_count(response, tail)


def main(args):
    """runs pwned_api_check and return results in text"""
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times.. you should replace your password!')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    main(sys.argv[1:])