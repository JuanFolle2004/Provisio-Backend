<?php

declare(strict_types=1);

namespace Src\Shared\App\Exceptions\Http;

class InvalidActionException extends HttpException
{
    /**
     * The HTTP status code.
     */
    protected int $status = 422;

    /**
     * The error code.
     */
    protected string $errorCode = 'invalid_action';

    /**
     * The error message.
     *
     * @var string
     */
    protected $message = 'This is an invalid action';
}
