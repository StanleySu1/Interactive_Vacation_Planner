# Interactive Vacation Planner

## Members

- Bowen Shan (bs7)
- Hongjiang Ye (ye36)
- Kelvin Chong (kvchong2)
- Stanley Su (ssu603)

### Setup
```
conda create -n project python=3.12
conda activate project
pip install -r requirements.txt
```

Install ollama from https://ollama.com/

Use quantized llama3.2:3b
```
ollama run llama3.2
```


### Data processing
```
./scrape.sh
./dataprep.sh
./run.sh
```

### Sample Interaction (from run.sh)
```
 My name is Bob and I'm a travel concierge here to assist you in planning your next adventure.

Where are you off to? Are you looking for some culture, history, or perhaps something more adventurous? What type of activities are you intere
sted in?
> I wanna see animals in vegas!
Las Vegas animals
It looks like Las Vegas has plenty of exciting options for animal lovers. Here are some recommendations:

If you're interested in seeing sharks, I'd recommend visiting the Shark Reef Aquarium or SeaQuest. Both of these attractions offer a unique underwater experience where you can get up close and personal with a variety of shark species.

If you're looking for something more interactive, Dig This is a great option. You'll have the chance to drive real earth-moving machines like bulldozers and excavators, which could be a fun and unique experience.

For a more relaxing experience, the Flamingo Wildlife Habitat is a beautiful outdoor exhibit that's home to many birds, fish, and turtles. It's free to visit and open every day of the year.

Lastly, if you're interested in seeing some exotic animals like Komodo dragons and piranhas, Shark Reef Aquarium might be the way to go.

Which one of these options sounds most appealing to you?
> Tell me more about shark reef. When does it close?
Las Vegas shark reef aquarium
It looks like Shark Reef Aquarium is a popular attraction in Las Vegas. Here's more information about it:

**Last Admission Time:** 7:00 PM (please note that this may be subject to change, so it's always best to check with the aquarium directly for the most up-to-date information)

**Opening Hours:** The aquarium is open daily from 10:00 AM to 8:00 PM.

**Exhibits and Animals:** Shark Reef Aquarium features over 2,000 animals from around the world, including sharks, rays, sea turtles, piranhas , and a Komodo dragon. You'll also get to see a variety of fish species, coral, and other marine life.

**Diving Experience:** One of the unique aspects of Shark Reef Aquarium is its diving experience. You can take a guided tour or rent equipment to dive with the sharks and other marine animals in their natural habitat.

**Tips and Reminders:**

* Make sure to check the aquarium's website for any special events or closures before planning your visit.
* Wear comfortable shoes, as you'll be doing some walking around the exhibit.
* Bring a camera to capture all the amazing sights and creatures!
* Don't forget to ask about any interactive experiences or feeding demonstrations during your visit.

I hope this helps! Are there any other questions you have about Shark Reef Aquarium?
>
```