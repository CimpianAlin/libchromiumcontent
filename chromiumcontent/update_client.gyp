{
  'targets': [
    {
      'target_name': 'update_client',
      'type': 'none',
      'dependencies': [
        '<(DEPTH)/courgette/courgette.gyp:courgette_lib',
        '<(DEPTH)/components/components.gyp:component_updater',
        '<(DEPTH)/components/components.gyp:client_update_protocol',
        '<(DEPTH)/components/components.gyp:update_client',
        '<(DEPTH)/components/components.gyp:version_info',
        '<(DEPTH)/third_party/lzma_sdk/lzma_sdk.gyp:lzma_sdk',
        '<(DEPTH)/third_party/zlib/google/zip.gyp:zip',
      ]
    }
  ]
}

