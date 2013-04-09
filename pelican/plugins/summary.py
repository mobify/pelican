"""
Slightly customized summary plugin that allows for empty summaries.

"""
import types

from pelican import signals

def initialized(pelican):
    from pelican.settings import _DEFAULT_CONFIG
    _DEFAULT_CONFIG.setdefault('SUMMARY_BEGIN_MARKER',
                               '<!-- PELICAN_BEGIN_SUMMARY -->')
    _DEFAULT_CONFIG.setdefault('SUMMARY_END_MARKER',
                               '<!-- PELICAN_END_SUMMARY -->')
    if pelican:
        pelican.settings.setdefault('SUMMARY_BEGIN_MARKER',
                                    '<!-- PELICAN_BEGIN_SUMMARY -->')
        pelican.settings.setdefault('SUMMARY_END_MARKER',
                                    '<!-- PELICAN_END_SUMMARY -->')

def content_object_init(self_class, instance):
    # If summary is already specified, use it.
    if 'summary' in instance.metadata:
        return

    # Override `_get_content` to remove summary markers.
    def _get_content(self):
        content = self._content
        if self.settings['SUMMARY_BEGIN_MARKER']:
            content = content.replace(
                self.settings['SUMMARY_BEGIN_MARKER'], '', 1)
        if self.settings['SUMMARY_END_MARKER']:
            content = content.replace(
                self.settings['SUMMARY_END_MARKER'], '', 1)
        return content
    instance._get_content = types.MethodType(_get_content, instance)

    content = instance._content
    if hasattr(instance, '_summary') or content is None:
        return

    # The the summary.
    start = -1
    end = -1

    if instance.settings['SUMMARY_BEGIN_MARKER']:
        start = content.find(instance.settings['SUMMARY_BEGIN_MARKER'])

    if instance.settings['SUMMARY_END_MARKER']:
        end = content.find(instance.settings['SUMMARY_END_MARKER'])

    if start != -1 or end != -1:
        # the beginning position has to take into account the length
        # of the marker
        start = (start + len(instance.settings['SUMMARY_BEGIN_MARKER']) if start != -1 else 0)
        end = end if end != -1 else None
        instance._summary = content[start:end]

    # Set an empty summary so templates can detect whether one was explictly set.
    # @jb: We can't use `None` here as something throws an error later on.
    else:
        instance._summary = ""


def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(content_object_init)