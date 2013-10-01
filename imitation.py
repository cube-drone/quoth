
import json
import urllib2
import random

target_server = "http://curtis.lassam.net/pierc/web/json.php"

def load_list_of_names( ):
    url = target_server + "?type=list_users"
    names = getJSON( url )
    names = sorted( names, key=lambda name: name.lower() )
    return names


def load_data_for_user( username, n ):
    url = target_server + "?type=user&user="+username+"&n="+str(n)
    data = [ x['message'] for x in getJSON( url )]
    print len(data)
    return data
    

def getJSON( url ):
    request = urllib2.Request( url )
    
    try:
        response = urllib2.urlopen(request)
        return json.loads( response.read() )
    except urllib2.HTTPError as e:
        try:
            error = e.read()
            print error
        except:
            return error

def save_to_file( data, filename ):
    with file(filename, 'w') as f:
        f.write( data )

def load_user(username):
    print slugify(username)
    save_to_file(json.dumps(load_data_for_user( username, 50000 ), indent=4), 'user_data/'+slugify(username)+'.json')

def mass_load():
    for user in load_list_of_names():
        load_user(user)

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join( [c for c in value if c in valid_chars] )

with file( "all_names.json", 'r') as f: 
    all_names = json.loads( f.read() )

def quote__(user):
    """
    Return a random saying by this user
    """
    try:
        if len(user.split()) > 1:
            user = user.split()[-1]
        if not user in all_names:
            user = random.choice(all_names)
        with file( "user_data/"+slugify(user)+".json", 'r') as f:
            quote = random.choice( json.loads( f.read() ) )
        return quote
    except:
        return ""

def strip_names( quote ):
    for name in all_names:
        quote = quote.replace( name +": " , "NAME: " )
    return quote

def empty_or_ping_timeout(quote):
    if quote == "" or quote == " " or quote.startswith("Ping") or quote.startswith("Read error"):
        return True
    return False

def quote(user):
    attempts = [strip_names(quote__(user)) for x in range(0, 8)]
    attempts = [x for x in attempts if not empty_or_ping_timeout(x)]
    if len(attempts) > 0:
        return max( attempts, key= lambda x: len(x) )
    else:
        return " um.. " 

if __name__ == "__main__":
    # mass_load()
    load_user('n0ob')
