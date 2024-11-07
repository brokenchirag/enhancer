from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageEnhance
import io

# Bot token from BotFather
TOKEN = "7933257531:AAG5iUv16JRGOGEHI-DgPKR0tqiy5rgNswM"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me an image, and I'll enhance it for you!")

def enhance_image(image_data: bytes) -> bytes:
    # Open the image
    image = Image.open(io.BytesIO(image_data))

    # Enhance the image (you can adjust this as needed)
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(2.0)  # Increase contrast (adjust value as needed)

    # Save the enhanced image to a byte array
    byte_io = io.BytesIO()
    enhanced_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    return byte_io

def handle_image(update: Update, context: CallbackContext) -> None:
    # Get the file sent by the user
    file = update.message.photo[-1].get_file()
    file.download("received_image.jpg")

    # Process the image and enhance it
    with open("received_image.jpg", "rb") as f:
        image_data = f.read()
        enhanced_image = enhance_image(image_data)

    # Send back the enhanced image
    update.message.reply_photo(photo=enhanced_image)

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
