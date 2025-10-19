<?php

declare(strict_types=1);

namespace Src\Shared\App\Exceptions\Http;

/**
 * An exception thrown whan a page is not found.
 */
class PageNotFoundException extends HttpException
{
    protected int $status = 404;

    protected string $errorCode = 'page_not_found';
}
