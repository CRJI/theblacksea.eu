from wagtail.core.blocks.struct_block import StructValue
from .. import models
from ..models.streamfield import StoryStreamBlock


def handle(user, pk, out):
    story = models.Story.objects.all().get(pk=pk)
    changed = False
    new_body = []
    for item in story.body:
        block_type = item.block.name
        if block_type == 'embedded_image':
            block_type = 'image'
            new_value = StructValue(StoryStreamBlock.base_blocks['image'])
            new_value['image'] = item.value['image']
            new_value['caption'] = item.value['caption']
            new_value['alignment'] = 'medium'
            changed = True

        else:
            new_value = item.value

        new_body.append((block_type, new_value))

    if changed:
        print(f"Saving {story.url}", file=out)
        story.body = new_body
        story.save_revision(user=user)

    else:
        print(f"Nothing to change for {story.url}", file=out)
