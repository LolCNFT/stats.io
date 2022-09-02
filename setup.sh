mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]
# Primary color
primaryColor = '#924078'
backgroundColor='#000908'
secondaryBackgroundColor='#28426c'
textColor='#fffff'
font='sans serif'
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml