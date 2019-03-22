# pylint: disable=no-value-for-parameter

import click

from utils.misc import delfile
from utils.configs import validate, parse_yaml_config
from utils.cert import prepare_ca, SSL_CERT_KEY_PATH, SSL_CERT_PATH, get_secret_key, copy_ssl_cert, copy_secret_keys
from utils.db import prepare_db
from utils.jobservice import prepare_job_service
from utils.registry import prepare_registry
from utils.registry_ctl import prepare_registry_ctl
from utils.core import prepare_core
from utils.notary import prepare_notary
from utils.log import prepare_log_configs
from utils.clair import prepare_clair
from utils.chart import prepare_chartmuseum
from utils.docker_compose import prepare_docker_compose
from utils.nginx import prepare_nginx, nginx_confd_dir
from g import (config_dir, config_file_path, private_key_pem_path, root_crt_path,
registry_custom_ca_bundle_storage_path, registry_custom_ca_bundle_storage_input_path, secret_key_dir,
old_private_key_pem_path, old_crt_path)

# Main function
@click.command()
@click.option('--conf', default=config_file_path, help="the path of Harbor configuration file")
@click.option('--with-notary', is_flag=True, help="the Harbor instance is to be deployed with notary")
@click.option('--with-clair', is_flag=True, help="the Harbor instance is to be deployed with clair")
@click.option('--with-chartmuseum', is_flag=True, help="the Harbor instance is to be deployed with chart repository supporting")
def main(conf, with_notary, with_clair, with_chartmuseum):

    delfile(config_dir)
    config_dict = parse_yaml_config(conf)
    validate(config_dict, notary_mode=with_notary)

    prepare_log_configs(config_dict)
    prepare_nginx(config_dict)
    prepare_core(config_dict, with_notary=with_notary, with_clair=with_clair, with_chartmuseum=with_chartmuseum)
    prepare_registry(config_dict)
    prepare_registry_ctl(config_dict)
    prepare_db(config_dict)
    prepare_job_service(config_dict)

    copy_secret_keys()
    get_secret_key(secret_key_dir)

    if config_dict['protocol'] == 'https':
        copy_ssl_cert()

    #  If Customized cert enabled
    prepare_ca(
        private_key_pem_path=private_key_pem_path,
        root_crt_path=root_crt_path,
        old_private_key_pem_path=old_private_key_pem_path,
        old_crt_path=old_crt_path,
        registry_custom_ca_bundle_config=registry_custom_ca_bundle_storage_input_path,
        registry_custom_ca_bundle_storage_path=registry_custom_ca_bundle_storage_path)

    if with_notary:
        prepare_notary(config_dict, nginx_confd_dir, SSL_CERT_PATH, SSL_CERT_KEY_PATH)

    if with_clair:
        prepare_clair(config_dict)

    if with_chartmuseum:
        prepare_chartmuseum(config_dict)

    prepare_docker_compose(config_dict, with_clair, with_notary, with_chartmuseum)

if __name__ == '__main__':
    main()