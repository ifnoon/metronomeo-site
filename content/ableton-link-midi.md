# Use Ableton Link and MIDI with an iPhone metronome

Ableton Link and MIDI solve different problems in a practice setup. Link lets compatible apps share tempo and musical alignment. MIDI can let a controller or foot pedal operate the metronome without touching the screen. Choose the connection for the job rather than treating every cable, network and Bluetooth device as the same kind of sync.

This guide describes Metronomeo on iPhone and iPad. Link and MIDI controls require Metronomeo Pro. Begin with a simple click, then add other tools only after you can explain which device controls tempo and which control starts or stops playback.

## Choose the connection you need

| Goal | Connection | What to expect |
| Share tempo with a compatible app | Ableton Link | Shared tempo and beat alignment over a local network |
| Start or stop with a pedal | MIDI note or Control Change assignment | A learned message triggers an action |
| Turn a hardware knob to change tempo | MIDI Control Change assignment | Values map across your selected tempo range |
| Copy playlists to another device | iCloud library sync | Library data, not musical timing |

Metronomeo's MIDI assignments are remote controls, not MIDI Clock synchronization. Pairing a Bluetooth speaker also does not create a MIDI input. Keep these distinctions in mind when a device appears connected but does not perform the action you expected.

## Join an Ableton Link session

Connect the iPhone or iPad and the other device to the same reachable local network. Open Settings, then Ableton Link in Metronomeo. Use the Ableton Link button to open the official settings panel and enable Link. Enable Link in the other compatible app too, allowing local network access where requested.

In Ableton Live, enable Link in its Link settings or the control bar. The exact settings tab name depends on the Live version. You do not need a Live project to connect two other compatible Link apps; Live is one possible participant, not a requirement for every session.

Change the shared tempo slightly in one app and check that the other follows. Start with a simple musical reference before introducing a complicated meter or practice plan. Anyone in a Link session can affect its tempo, so an unexpected change may come from another participant.

## Choose how the local click follows Link

Metronomeo's Click note setting controls its relationship to Link's shared quarter note grid. A quarter note gives one local click per Link beat. An eighth note gives two, and a sixteenth note gives four. A half note gives one click every two Link beats.

If the apps share a tempo but Metronomeo clicks twice as often, inspect Click note before assuming synchronization is broken. Changing the local click relationship does not ask the other apps to change the shared tempo.

Follow meter ties the alignment cycle to your current measure. If the session needs a fixed cycle instead, turn it off and choose Quarter notes. For example, four quarter notes represents a standard four beat bar. Start with the default relationship unless your musical setup needs something different.

## Treat shared start and stop as a separate choice

Link tempo synchronization does not require every app to start and stop together. The official Link panel has a start and stop synchronization option. Enable shared transport deliberately in the participating apps and test it before relying on a pedal or another performer to start a session.

Metronomeo uses Link for timing. It does not provide Link Audio streaming, share sound presets or copy playlists through Link. If you want to hear another device's audio, arrange an appropriate audio connection separately. If you want the same library, use iCloud sync instead.

## Learn a MIDI pedal or button

Open Settings, then MIDI, and enable MIDI. Connect a compatible USB controller or interface with the adapter your device needs. For Bluetooth MIDI, use the Bluetooth option in MIDI settings and connect the controller through Apple's device picker.

1. Open Input log and press the controller's button. Confirm that a message arrives.
2. Find the desired action under Assignments, such as Play / Stop, Start, Stop or Next song.
3. Tap Learn, then press the button or MIDI foot switch you want to assign.
4. Return to the main screen and test the action once while stopped, then during playback if relevant.
5. If the action does not fire, check its MIDI channel, source and assignment rather than repeatedly reconnecting a working device.

An ordinary sustain pedal needs a MIDI controller or interface that converts its operation into an appropriate message. Plugging an unrelated foot switch into an audio connection does not make it a MIDI control.

## Assign a tempo knob

Choose Learn for Absolute tempo (CC), then move a knob or fader that sends Control Change. Metronomeo maps the controller's values from zero through 127 onto the Minimum and Maximum under Tempo range. A smaller musical range gives you finer control over the interval you actually use.

A note message cannot act as this absolute control. If the input is already assigned elsewhere, resolve the overlapping assignment so one movement does not unexpectedly trigger two actions. Test slowly before using the control during a rehearsal.

## Troubleshoot one layer at a time

If Link peers are missing, check that both apps have Link enabled, have local network permission and can reach each other on the same network. Guest networks or isolated clients can prevent discovery. A Bluetooth audio connection is not a Link network connection.

If the tempo matches but the click sounds late, try the device speaker or a wired output. Wireless audio latency is different from a wrong tempo. Avoid changing the tempo to compensate for a delayed audio route.

If tempo moves unexpectedly, check Link peers, a running tempo plan and learned MIDI controls. Starting a tempo plan in Metronomeo pauses Link synchronization so the plan can control tempo. Give one mechanism a clear role before combining several controls.
