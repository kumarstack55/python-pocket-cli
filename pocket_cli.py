#!/usr/bin/env python
# coding: utf-8

import argparse
from pocketlib import PocketClient
from pocketlib import get_consumer_key
from pocketlib import get_access_token


def handler_retrieve(client, args):
    json_text = client.retrieve(
        state=args.state,
        favorite=args.favorite,
        tag=args.tag,
        content_type=args.content_type,
        detail_type=args.detail_type,
        search=args.search,
        domain=args.domain,
        since=args.since,
        count=args.count,
        offset=args.offset)
    print(json_text)


def handler_add(client, args):
    json_text = client.add(
        url=args.url,
        title=args.title,
        tags=args.tags,
        tweet_id=args.tweet_id)
    print(json_text)


def _get_parser_retrieve(subparsers):
    p = subparsers.add_parser('retrieve')
    p.add_argument('--state', type=str)
    p.add_argument('--favorite', type=int)
    p.add_argument('--tag', type=str)
    p.add_argument('--content-type', type=str)
    p.add_argument('--detail-type', type=str)
    p.add_argument('--search', type=str)
    p.add_argument('--domain', type=str)
    p.add_argument('--since', type=int)
    p.add_argument('--count', type=int)
    p.add_argument('--offset', type=int)
    p.set_defaults(handler=handler_retrieve)


def _get_parser_add(subparsers):
    p = subparsers.add_parser('add')
    p.add_argument('--url', type=str, required=True)
    p.add_argument('--title', type=str)
    p.add_argument('--tags', type=str)
    p.add_argument('--tweet-id', type=str)
    p.set_defaults(handler=handler_add)


def get_arg_parser():
    p = argparse.ArgumentParser()

    group = p.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', default=True)
    group.add_argument('--force', dest='dry_run', action='store_false')

    p.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = p.add_subparsers()
    _get_parser_retrieve(subparsers)
    _get_parser_add(subparsers)

    return p


def main():
    parser = get_arg_parser()

    consumer_key = get_consumer_key()
    access_token = get_access_token()
    client = PocketClient(consumer_key, access_token)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(client, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
