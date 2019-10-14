from flaskblog import app

import os
if __name__ == "__main__":
	print('validate line credential!\n.\n.\n.')
	print('line channel secret:' + os.getenv('LINE_CHANNEL_SECRET'))
	print('line channel access token:' + os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
	print('validate database credential!\n.\n.\n.')
	print('database url:' + os.getenv('DATABASE_URL'))
	print('validate cloudinary credential!\n.\n.\n.')
	print('cloudinary key:' + os.getenv('CLOUDINARY_KEY'))
	print('cloudinary secret' + os.getenv('CLOUDINARY_SECRET'))
	port = int(os.environ.get('PORT', 5001))
	app.run(host='0.0.0.0', port=port)
