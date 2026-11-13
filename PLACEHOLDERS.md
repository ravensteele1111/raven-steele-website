# What is still missing

Updated 13 November 2026, after the first round of answers came back.

Most of the words and every link are now real. What is left is pictures, prices and a
handful of specifics.

---

## 1. Pictures, the big one

**No photos have arrived yet.** Every grey dashed box on the site is a real gap. The
Google Drive folder link was left blank on the form.

Nothing else on the site matters as much as this. It is the difference between a layout
and a website.

- [ ] **HERO** - Raven on stage. A video loop or a tall photo. First thing anyone sees
- [ ] **STORY-RAVEN-AND-ETHAN**, **STORY-WIDE** - the two of them
- [ ] **CAST portraits x8** - Raven, Ethan, Lucky, Zeus, Baby Rebel, Jordyn, Betty, Sprout
- [ ] **EVENT covers x6** - one per event
- [ ] **EVENT photos** - eight or more per event, each marked goofy, sweet or action
- [ ] **EVENT group shots x6**
- [ ] **SKOOL icons x4** - Revenue Revolution, AI for Beginners, Digital Marketing 4
      Beginners, Digital Products with Claude. The customer asked for the real icons, and
      the tiles are built to lead with the picture
- [ ] **PRODUCT pictures x5** - the best seller plus four

## 2. The shop

**29 products on the site.** Filters are Tools, Prompts and Meme Bots. No prices anywhere:
the price is on the product page, so it changes without anybody touching this website.

**The 14 Toolboxes are off the site.** Blue clicked three by hand on 13 November and none
of them opened, so all fourteen came down rather than leaving dead links up. They are
hidden in `products.json`, not deleted: delete the `hide` flag, rerun `build-shop.py`, and
they are back in seconds.

`products.json` holds the lot and `build-shop.py` writes the page. Removing a product is
deleting four lines of data and running it again.

**How far the checking actually got, honestly:**

- **Eleven were confirmed to open from here.** Then Beacons started refusing this machine
  entirely, after roughly a hundred requests from one address. That is rate limiting, not
  broken products: The Sales Page Builder answered 200 and then 403 within the hour
- **The fourteen Toolboxes are genuinely broken, not just unreachable from here.** This
  machine could not get a TLS handshake out of `revenuerevolution.store` at all, so the
  three test links went to Blue, and none of the three opened in a real browser either.
  That settles it: the addresses are wrong or the pages are gone
- [ ] **Working Toolbox addresses.** Fourteen products are written, named and carry their
      taglines, waiting on addresses that load. Worth asking whether they live on Beacons
      like everything else, rather than on `revenuerevolution.store`

Still missing:

- [ ] **Pictures for 35 of the 43.** Eight have their artwork
- [ ] **Which one is the best seller.** The block is on the page waiting for a name

## 3. Words still open

- [ ] **`[YOUR FREE STARTER GIFT]`** on Be Like Raven. The main free gift is answered,
      photos that never go on Instagram plus every new song first, but this second one
      was left blank. Same thing, or different?
- [ ] **`[ONE LINE]`** for AI for Beginners. The other three Skools have their line
- [ ] **`[NEXT CHAPTER TITLE]`** - chapter 13, shown dimmed as coming next
- [ ] **Dates and stories for three events** - Donuts With Mom, Haunted Carnival and
      Insta Jail have names only
- [ ] **`[MORE GUESTS]`** - the guest lists for five of the six events are marked
      incomplete. Love at First Trivia is the only full one

## 4. Waiting on somebody else's permission

- [ ] **The two Rebel wins are written and NOT on the site.** The answers came with
      "ask her before it goes live", so the two members' quotes are deliberately held
      back. The repository is public, and a real person's name and words do not go up
      without their yes. The text is ready the moment it comes

## 5. Pictures from Instagram: what we can take and what we cannot

Tested 13 November, not assumed.

**Reels and posts: we can take the cover frame ourselves.** Instagram still answers
`/p/<code>/media/?size=l` with the real frame and no login. The mirror video chapter
already shows it, gold dress and tuxedo. `fetch-ig.py` does it for any reel or post
address, and the picture is downloaded and kept, because the addresses Instagram hands
back expire within days.

**So: send a reel or post address and the picture arrives free.**

- [ ] **Reel or post addresses for the other chapters.** Only the mirror video has one so
      far. Every chapter with a reel behind it can have a picture at no cost to anybody

**Highlights: we cannot.** A highlight is a collection rather than a post, so there is no
code to ask for, and the page behind it is a login wall. Confirmed by trying it.

- [ ] **Highlight covers have to come from the customer.** On a phone: open the highlight,
      tap Edit highlight, and the cover can be saved from there. Eleven of them: Camping
      Chaos, First Date Disaster, Bury the Problem, The Saga, Hale's Secret, Ethan Music,
      Sprout, Second Date, Music, The third Date, The Meadows

## 6. Waiting on the customer, from round two

- [ ] **The Google Drive link for the photos.** It was blank on the form and there is no
      link anywhere in the document. Nothing can be swapped in until it arrives
- [ ] **Instagram highlight links.** Almost everything is in the highlights, and the
      chapters and mini stories should point at them. Instagram highlight addresses look
      like `instagram.com/stories/highlights/<number>/` and cannot be guessed, so the
      customer needs to open each highlight and copy the address
- [ ] **Is a Lyrics button wanted at all?** The lyrics are in every YouTube description,
      so the button was removed rather than left saying "Soon". Easy to put back

## 7. Noted, not built

- **Locking the extras behind signing up.** The idea: join the email list and you get
  access to the extra event photos and so on. Written down on purpose and not started.
  It would mean every page is public except some photos, which needs either a password
  everyone shares or real accounts. Worth a proper conversation before any of it is built

## 8. Questions the answers raised

- [ ] **"Where It Better" is spelled that way on YouTube.** The customer said the title
      should be **Wear It Better**. The video's own title on YouTube reads "Where It
      Better", so the typo is on YouTube and not in anything we were sent. The site
      currently matches YouTube. Fix the video title and the site follows
- [ ] **There are no Ethan solo songs.** 26 songs are on the Music page: 6 duets and 19
      of Raven's. The Ethan filter is built, as the design asked, and currently shows
      "nothing in that one yet". Are his coming, or should the filter go?
- [ ] **"The Meadows"** is one of Raven's Instagram highlights but was not matched to a
      chapter. Which part of the story is it?
- [ ] **Every event is 2026**, so the year filter is just Newest and 2026. The 2025 chip
      came out and goes back the moment there is an older event
- [ ] **Chapter titles** - six were renamed to match the Instagram highlights: First
      Date, Second Date, The 3rd Date, The Saga, Hale's Secret, Sprout. Six kept the
      names written here: the night he saw her on stage, the white shirt, the recording
      studio, the mirror video, Jamaica, babysitting

## 9. Legal

The Privacy, Terms and Cookies questions came back blank, so those pages are not built
and the footer links still go nowhere.

What we do have: **Marketing Ambition PTY LTD, Australia**, and
**aiinfluencerraven@gmail.com** as the contact. That is everything needed to write them
the moment the answer is yes.

## 10. The email list

Still not connected. The form works, the Watch / Listen / Learn tagging works, and
submitting says so plainly. It needs an account in the customer's name.

---

## Standing note

The customer's last line on the form: *"Make the Skools big picture tiles using each
school's real icon, not text cards. Raven is very visual, so more pictures everywhere and
less text."*

The Skool tiles are rebuilt that way. The rest of that instruction is waiting on photos.
Once they arrive, the pages get more picture and less text throughout.
