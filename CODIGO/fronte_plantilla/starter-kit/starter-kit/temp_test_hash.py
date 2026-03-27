from app.core.security import get_password_hash, verify_password
for pw in ['test123', 'a'*200, 'ñ'*50]:
    try:
        h = get_password_hash(pw)
        print('OK', pw[:10], len(pw.encode('utf-8')), '->', len(h))
        print('verify', verify_password(pw, h))
    except Exception as e:
        print('ERR', pw[:10], type(e), e)
